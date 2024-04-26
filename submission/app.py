import os
import shutil
import argparse
import pandas as pd
from zipfile import ZipFile
from autogluon.tabular import TabularPredictor

def parse_args():

    # Create the parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--id-column', dest='id_column', type=str, help='column that should be used to join files')
    parser.add_argument('--target_column', dest='target_column', type=str, help='column representing the value that is being predicted over')
    parser.add_argument('--model', dest='model', type=str, help='Path to pretrained model to use')
    parser.add_argument('--dataset', dest='dataset', type=str, help='Path to zip file representing your dataset')

    # Parse the arguments and return:
    return parser.parse_args()

def make_df(path, id_column):

    # Initialize df to empty dataframe (will assemble incrementally):
    df = pd.DataFrame()

    # Iterate over all files in dataset subdirectory:
    for filename in os.listdir(path):

        # Determine filetype and character separator:
        if filename.endswith('.csv'):
            sep = ','
        elif filename.endswith('.tsv'):
            sep = '\t'
        else:
            raise('Files must be either tsv or csv')
        
        # Get full filepath and read file into temp dataframe:
        file = os.path.join(path, filename)
        temp = pd.read_csv(file, sep=sep)

        # If id-column is not in dataframe, assume file needs to be transposed:
        if id_column not in temp.columns:
            temp = temp.transpose().reset_index().rename(columns={'index':id_column})
        
        # If file is first file, assign to dataframe, otherwise merge on id-column:
        if df.empty:
            df = temp
        else:
            df = pd.merge(df, temp, on=id_column, how='inner')

    # Return:
    return df

def get_confusion_matrix(predictions, ground):

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(predictions)):
        try:
            if predictions[i] == 1 and predictions[i] == ground[i]:
                TP += 1
            if predictions[i] == 0 and predictions[i] == ground[i]:
                TN += 1
            if predictions[i] == 1 and predictions[i] != ground[i]:
                FP += 1
            if predictions[i] == 0 and predictions[i] != ground[i]:
                FN += 1
        except:
            'Skipping row: ' + str(i)

    return TP, TN, FP, FN

def get_metrics(TP, TN, FP, FN):

    if TP + FP > 0:
        precision = TP / (TP + FP)
    else:
        precision = 0
    
    if TP + FN > 0:
        recall = TP / (TP + FN)
    else:
        recall = 0

    if TP + TN + FP + FN > 0:
        accuracy = (TP + TN) / (TP + TN + FP + FN)
    else:
        accuracy = 0

    if FP + TN > 0:
        specificity = TN / (FP + TN)
    else:
        specificity = 0
    
    if precision + recall > 0:
        f1 = (2 * precision * recall) / (precision + recall)
    else:
        f1 = 0

    return precision, recall, accuracy, specificity, f1

def get_auroc(predictor, data, ground, N):

    auroc = 0
    for i in range(N):
        predictions = predictor.predict(data, decision_threshold=(i+1)/N)
        TP, TN, FP, FN = get_confusion_matrix(predictions, ground)
        precision, recall, accuracy, specificity, f1 = get_metrics(TP, TN, FP, FN)
        auroc += recall / N

    return auroc

def get_metrics_string(predictions, ground, auroc):

    TP, TN, FP, FN = get_confusion_matrix(predictions, ground)
    precision, recall, accuracy, specificity, f1 = get_metrics(TP, TN, FP, FN)
    
    metric_string = f"precision,{precision}\nrecall,{recall}\naccuracy,{accuracy}\nspecificity,{specificity}\nF1,{f1}\nAUROC,{auroc}\n"
    metric_string += f'TP,{TP}\nTN,{TN}\nFP,{FP}\nFN,{FN}\n'
    return metric_string

if __name__ == '__main__':

    # Parse arguments:
    args = parse_args()
    dataset: str = os.getenv('DATASET') or args.dataset
    model: str = os.getenv('MODEL') or args.model
    id_column: str = os.getenv('ID_COLUMN') or args.id_column
    target_column: str = os.getenv('TARGET_COLUMN') or args.target_column

    # Extract dataset:
    with ZipFile(dataset) as zObject:
        zObject.extractall(path = os.getcwd() + '/extracted_dataset')

    # Extract model:
    if model:
        with ZipFile(model) as zObject:
            zObject.extractall(path = os.getcwd() + '/output')
    
    # Dive into dataset folder structure:
    base_dataset_path = os.getcwd() + '/extracted_dataset'
    base_dataset_subfolders = [f.path for f in os.scandir(base_dataset_path) if f.is_dir()]
    if f'{base_dataset_path}/train' in base_dataset_subfolders:
        dataset_path = base_dataset_path # If dataset was assembled programmatically, it will be here
    else:
        dataset_path = base_dataset_subfolders[0] # Otherwise it will be one level deeper
    
    # Acquire dataframes for training, eval, and testing data:
    train_df = make_df(f'{dataset_path}/train', id_column)
    eval_df = pd.DataFrame()
    if os.path.exists(f'{dataset_path}/eval'): # Eval set is optional
        eval_df = make_df(f'{dataset_path}/eval', id_column)
    test_df = make_df(f'{dataset_path}/test', id_column)

    # Preprocessing:
    for df in [train_df, eval_df, test_df]:
        if target_column in df.columns:
            df.dropna(subset=[target_column], inplace=True)

    # If passing in pretrained model, load model:
    if model:
        print('Using existing model...')
        predictor = TabularPredictor(label=target_column, problem_type="binary", eval_metric="f1", path=os.getcwd()+"/output/models").load(os.getcwd() + '/output/models')
 
    # Otherwise, train new model:
    else:
        print('Training new model...')
        predictor = TabularPredictor(label=target_column, problem_type="binary", eval_metric="f1", path=os.getcwd()+"/output/models").fit(train_data=train_df, presets='best_quality')

    # Acquire predictions and metrics for train set:
    y_train = train_df[target_column]
    x_train = train_df.drop([target_column], axis=1)
    p_train = predictor.predict(x_train)
    r_train = get_auroc(predictor, x_train, y_train, 10)
    m_train = get_metrics_string(p_train, y_train, r_train)

    # Acquire predictions and metrics for eval set:
    if not eval_df.empty:
        y_eval = eval_df[target_column]
        x_eval = eval_df.drop([target_column], axis=1)
        p_eval = predictor.predict(x_eval)
        r_eval = get_auroc(predictor, x_eval, y_eval, 10)
        m_eval = get_metrics_string(p_eval, y_eval, r_eval)

    # Acquire predictions for test set:
    p_test = predictor.predict(test_df)
    if target_column in test_df.columns:
        y_test = test_df[target_column]
        x_test = test_df.drop([target_column], axis=1)
        r_test = get_auroc(predictor, x_test, y_test, 10)
        m_test = get_metrics_string(p_test, y_test, r_test)        

    # Write results to output file:
    with open(os.getcwd() + '/output/metrics.csv', 'w') as f:
        f.write('TRAIN\n')
        f.write(m_train)
        f.write('\n')
        if not eval_df.empty:
            f.write('EVAL\n')
            f.write(m_eval)
            f.write('\n')
        if target_column in test_df.columns:
            f.write('TEST\n')
            f.write(m_test)

    # Write test predictions to output file:
    with open(os.getcwd() + '/output/train_predictions.csv', 'w') as f:
        df = pd.concat([train_df[id_column], p_train], axis=1)
        df.to_csv(f, index=False)

    # Write test predictions to output file:
    if not eval_df.empty:
        with open(os.getcwd() + '/output/eval_predictions.csv', 'w') as f:
            df = pd.concat([eval_df[id_column], p_eval], axis=1)
            df.to_csv(f, index=False)
   
    # Write test predictions to output file:
    with open(os.getcwd() + '/output/test_predictions.csv', 'w') as f:
        df = pd.concat([test_df[id_column], p_test], axis=1)
        df.to_csv(f, index=False)
