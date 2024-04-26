import pandas

def get_confusion_matrix(predictions, ground):

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(predictions)):
        try:
            if predictions[i] == 1 and predictions[i] == ground[i]:
                print('I got row ' + str(i + 2) + ' right')
                TP += 1
            if predictions[i] == 0 and predictions[i] == ground[i]:
                print('I got row ' + str(i + 2) + ' right')
                TN += 1
            if predictions[i] == 1 and predictions[i] != ground[i]:
                print('I got row ' + str(i + 2) + ' wrong')
                FP += 1
            if predictions[i] == 0 and predictions[i] != ground[i]:
                print('I got row ' + str(i + 2) + ' wrong')
                FN += 1
        except:
            'Skipping row: ' + str(i)

    print('\n')
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

def get_metrics_string(predictions, ground):

    TP, TN, FP, FN = get_confusion_matrix(predictions, ground)
    precision, recall, accuracy, specificity, f1 = get_metrics(TP, TN, FP, FN)
    
    metric_string = f"precision,{precision}\nrecall,{recall}\naccuracy,{accuracy}\nspecificity,{specificity}\nF1,{f1}\nAUROC,{'-'}\n"
    metric_string += f'TP,{TP}\nTN,{TN}\nFP,{FP}\nFN,{FN}\n'
    return metric_string

def output_metrics_and_predictions(subset, df, id_column, target_column, predictions):

    # Write metrics:
    if subset != 'test':
        m = get_metrics_string(predictions, df['mismatch'])
        with open(f'./output/{subset}_metrics.csv', 'w') as f:
            f.write(f'{subset.upper()}\n')
            f.write(m)
            f.write('\n')
   
    # Write predictions:
    with open(f'./output/{subset}_predictions.csv', 'w') as f:
        df = pandas.concat([df[id_column], predictions], axis=1)
        df.to_csv(f, index=False)

def get_mismatches(gender_df, msi_df, post_df):

    predictions = {'sample': [], 'mismatch': []}
    for i in range(len(post_df)):

        # Get row from all 3 files (they line up):
        gender_row = gender_df.iloc[i]
        msi_row = msi_df.iloc[i]
        post_row = post_df.iloc[i]

        # Get sample, gender, and msi predictions and supposed data:
        sample = post_row['sample']
        pred_gender = gender_row['gender']
        said_gender = 1 if post_row['gender'] == 'Male' else 0
        pred_msi = msi_row['msi']
        said_msi = 1 if post_row['msi'] == 'MSI-High' else 0

        # Compute mismatches:
        predictions['sample'].append(sample)
        if pred_gender == said_gender and pred_msi == said_msi:
            predictions['mismatch'].append(0)
        else:
            predictions['mismatch'].append(1)

    # Return:
    predictions_df = pandas.DataFrame(predictions)
    return predictions_df['mismatch']

def main():

    for x in ['train', 'eval', 'test']:
        try:
            gender_df = pandas.read_csv(f'./gender/{x}_predictions.csv', sep=',')
            msi_df = pandas.read_csv(f'./msi/{x}_predictions.csv', sep=',')
            post_df = pandas.read_csv(f'./post/{x}/{x}.csv', sep=',')
            predictions = get_mismatches(gender_df, msi_df, post_df)
            output_metrics_and_predictions(x, post_df, 'sample', 'mismatch', predictions)
        except Exception as e:
            print('Skipping set: ' + x)

main()
        
