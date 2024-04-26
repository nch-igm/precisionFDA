import os
import pandas

def merge_train():

    # Read in files as dataframes:
    df_1 = pandas.read_csv('./data-prep/fda-proteomic/input/train/train_pro.tsv', sep='\t')
    df_2 = pandas.read_csv('./data-prep/fda-proteomic/input/train/train_cli.tsv', sep='\t')
    df_3 = pandas.read_csv('./data-prep/fda-proteomic/input/train/sum_tab_1.csv', sep=',')

    # Transpose proteomic tsv:
    df_1 = df_1.transpose().reset_index().rename(columns={'index':'sample'})

    # Merge:
    df_12 = df_1.merge(df_2, on='sample')
    return df_12.merge(df_3, on='sample')

def merge_test():

    # Read in files as dataframes:
    df_1 = pandas.read_csv('./data-prep/fda-proteomic/input/test/test_pro.tsv', sep='\t')
    df_2 = pandas.read_csv('./data-prep/fda-proteomic/input/test/test_cli.tsv', sep='\t')

    # Transpose proteomic tsv:
    df_1 = df_1.transpose().reset_index().rename(columns={'index':'sample'})

    # Merge:
    return df_1.merge(df_2, on='sample')

def get_gender_df(df):

    # Remove the mismatch column (if it exists) and the MSI column:
    if 'mismatch' in df:
        df = df.drop(columns=['msi', 'mismatch'])
    else:
        df = df.drop(columns=['msi'])

    # Convert gender column to binary:
    df['gender_flag'] = 1 * (df['gender'] == 'Male')
    df = df.drop(columns=['gender'])
    df = df.rename(columns={'gender_flag': 'gender'})

    return df

def get_msi_df(df):

    # Remove the mismatch column (if it exists) and the MSI column:
    if 'mismatch' in df:
        df = df.drop(columns=['gender', 'mismatch'])
    else:
        df = df.drop(columns=['gender'])

    # Convert gender column to binary:
    df['msi_flag'] = 1 * (df['msi'] == 'MSI-High')
    df = df.drop(columns=['msi'])
    df = df.rename(columns={'msi_flag': 'msi'})

    return df

def get_prediction_columns(df):

    if 'mismatch' in df:
        df = df[['sample', 'gender', 'msi', 'mismatch']]
    else:
        df = df[['sample', 'gender', 'msi']]
    return df

def separate_mismatches(df):

    df_0 = df[df['mismatch'] == 0]
    df_1 = df[df['mismatch'] == 1]
    return df_0, df_1