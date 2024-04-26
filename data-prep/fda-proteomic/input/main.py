import os
import pandas
import shutil
from merge import merge_train, merge_test, separate_mismatches, get_gender_df, get_msi_df, get_prediction_columns
from stratification import stratify
from overunder import under_sample_random, under_sample_stratify

# Functions:
def main():

    # Merge train and test from original FDA dataset:
    print('Reading...')
    train_df = merge_train()
    test_df = merge_test()
    print(train_df)
    print(test_df)

    # Separate mismatches:
    train_df, mismatch_df = separate_mismatches(train_df)
    
    # Split training into two via stratification, one to train and another for
    # metric evaluation (to avoid any pollution):
    print('Stratifying...')
    train_df, eval_df = stratify(0.8, train_df, columns=['gender', 'msi'])
    eval_df = pandas.concat([eval_df, mismatch_df])
    print(train_df)
    print(eval_df)
    print('\n')

    #-- FOR GENDER:
    train_gender_df = get_gender_df(train_df)
    eval_gender_df = get_gender_df(eval_df)
    test_gender_df = get_gender_df(test_df)

    #-- FOR MSI:
    train_msi_df = get_msi_df(train_df)
    eval_msi_df = get_msi_df(eval_df)
    test_msi_df = get_msi_df(test_df)

    #-- FOR POST:
    train_post_df = get_prediction_columns(train_df)
    eval_post_df = get_prediction_columns(eval_df)
    test_post_df = get_prediction_columns(test_df)

    # Output Gender
    print('Exporting...')
    train_gender_df.to_csv(f'./data-prep/fda-proteomic/output/train/train.csv', index=False)
    eval_gender_df.to_csv(f'./data-prep/fda-proteomic/output/eval/eval.csv', index=False)
    test_gender_df.to_csv(f'./data-prep/fda-proteomic/output/test/test.csv', index=False)
    shutil.make_archive(f'./data-prep/fda-proteomic/datasets/fda_proteomic_gender_trial_1', 'zip', f'./data-prep/fda-proteomic/output')

    # Output MSI
    print('Exporting...')
    train_msi_df.to_csv(f'./data-prep/fda-proteomic/output/train/train.csv', index=False)
    eval_msi_df.to_csv(f'./data-prep/fda-proteomic/output/eval/eval.csv', index=False)
    test_msi_df.to_csv(f'./data-prep/fda-proteomic/output/test/test.csv', index=False)
    shutil.make_archive(f'./data-prep/fda-proteomic/datasets/fda_proteomic_msi_trial_1', 'zip', f'./data-prep/fda-proteomic/output')

    # Output Mismatch
    print('Exporting...')
    train_post_df.to_csv(f'./data-prep/fda-proteomic/output/train/train.csv', index=False)
    eval_post_df.to_csv(f'./data-prep/fda-proteomic/output/eval/eval.csv', index=False)
    test_post_df.to_csv(f'./data-prep/fda-proteomic/output/test/test.csv', index=False)
    shutil.make_archive(f'./data-prep/fda-proteomic/datasets/fda_proteomic_post_trial_1', 'zip', f'./data-prep/fda-proteomic/output')

# Main:
main()