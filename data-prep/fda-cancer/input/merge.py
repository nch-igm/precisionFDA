import os
import pandas

def merge_train():

    # Read in files as dataframes:
    df_1 = pandas.read_csv('./data-prep/fda-cancer/input/train/sc1_Phase1_GE_FeatureMatrix.tsv', sep='\t')
    df_2 = pandas.read_csv('./data-prep/fda-cancer/input/train/sc1_Phase1_GE_Phenotype.tsv', sep='\t')
    df_3 = pandas.read_csv('./data-prep/fda-cancer/input/train/sc1_Phase1_GE_Outcome.tsv', sep='\t')

    # Merge:
    df_12 = df_1.merge(df_2, on='PATIENTID')
    return df_12.merge(df_3, on='PATIENTID')

def merge_test():

    # Read in files as dataframes:
    df_1 = pandas.read_csv('./data-prep/fda-cancer/input/test/sc1_Phase2_GE_FeatureMatrix.tsv', sep='\t')
    df_2 = pandas.read_csv('./data-prep/fda-cancer/input/test/sc1_Phase2_GE_Phenotype.tsv', sep='\t')

    # Merge:
    return df_1.merge(df_2, on='PATIENTID')

def merge_train_peter():

    # Read in files as dataframes:
    df_1 = pandas.read_csv('./data-prep/fda-cancer/input/train/featureMatrixMedium.csv', sep=',')
    df_2 = pandas.read_csv('./data-prep/fda-cancer/input/train/sc1_Phase1_GE_Phenotype.tsv', sep='\t')
    df_3 = pandas.read_csv('./data-prep/fda-cancer/input/train/sc1_Phase1_GE_Outcome.tsv', sep='\t')

    # Transpose genes:
    df_1 = df_1.transpose().reset_index().rename(columns={'index':'PATIENTID'})

    # Merge:
    df_12 = df_1.merge(df_2, on='PATIENTID')
    return df_12.merge(df_3, on='PATIENTID')

def merge_special():

    old_train = pandas.read_csv('./data-prep/fda-cancer/input/prev/train/train.csv', sep=',')
    old_eval = pandas.read_csv('./data-prep/fda-cancer/input/prev/eval/eval.csv', sep=',')
    old_test = pandas.read_csv('./data-prep/fda-cancer/input/prev/test/test.csv', sep=',')

    peter = merge_train_peter()
    new_train = old_train[peter.columns]
    new_eval = old_eval[peter.columns]
    peter = peter.drop('SURVIVAL_STATUS', axis=1)
    new_test = old_test[peter.columns]

    return new_train, new_eval, new_test
