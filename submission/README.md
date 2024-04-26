This app is an advanced wrapper around AutoGluon TabularPredictor, and is capable of training new models on new tabular datasets and reporting predictions/performance, as well as using pre-existing models when specified.

#-- GENERIC AUTOGLUON TRAINING AND TESTING NEW MODELS:

1. Specify dataset zip folder (format should look as follows):
/<parent_folder_name>
    /train
        /file1.csv
        ...
        /fileN.csv
    /eval
        /file1.csv
        ...
        fileN.csv
    /test
        /file1.csv
        ...
        fileN.csv

*Note: .csv and .tsv are accepted*
*Note: eval set is optional*
*Note: test may or may not contain target_column*

2. Specify id_column (this is the identifier column for each row of data). As an example, the proteomic data has an id_column of 'sample'.

3. Specify target_column (this is the outcome column, or ground-truth/prediction column). As an example, the proteomic data has a target_column of 'mismatch'.

4. Specify output (directory where output results will go). There will be three result files, the first a 'metrics.csv' file with performance metrics (Precision, Recall, Accuracy, Specificity, F1, and confusion matrix) for each subset of data (train, eval if given, test if ground-truth provided). The second is a 'predictions.csv' which contains the predictions (model's predictions for the target_column) for the test set. The third is a 'model.zip' file, which contains the exported model (you can then reuse this for future invocations of the app if desired).

5. Click run. This will train a new model on the given data, then output results.

#-- USING PRETRAINED MODEL FOR FDA BRAIN CANCER:

1. You may either use the fda_brain_cancer_dataset.zip we have provided (pre-split for metric evaluation into train, eval, and test) or you can use your version of the dataset, so long as files are organized as described in the 'GENERIC' section.

2. model = fda_brain_cancer_model.zip (this is our pretrained model)

2. id_column = PATIENTID

3. target_column = SURVIVAL_STATUS

4. Specify output (directory where output results will go).

5. Click run. This will use the pretrained model, then output results.

#-- USING PRETRAINED MODEL FOR FDA PROTEOMIC:

1. You may either use the fda_proteomic_dataset.zip we have provided (pre-split for metric evaluation into train, eval, and test) or you can use your version of the dataset, so long as files are organized as described in the 'GENERIC' section.

2. model = fda_proteomic_model.zip (this is our pretrained model)

2. id_column = sample

3. target_column = mismatch

4. Specify output (directory where output results will go).

5. Click run. This will use the pretrained model, then output results.