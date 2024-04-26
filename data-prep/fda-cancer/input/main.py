import os
import pandas
import shutil
from merge import merge_train, merge_test
from stratification import stratify
from overunder import under_sample

# Functions:
def main():

    # Merge train and test from original FDA dataset:
    print('Reading...')
    train_df = merge_train()
    test_df = merge_test()
    print(train_df)
    print(test_df)
    
    # Split training into two via stratification, one to train and another for
    # metric evaluation (to avoid any pollution):
    print('Stratifying...')
    train_df, eval_df = stratify(0.8, train_df, columns=['CANCER_TYPE', 'SURVIVAL_STATUS'])
    print(train_df)
    print(eval_df)
    print('\n')

    # Under-sample majority class:
    print('Under Sampling...')
    train_df = under_sample(0.5, 1, 'SURVIVAL_STATUS', ['CANCER_TYPE', 'SURVIVAL_STATUS'], train_df)
    print(train_df)
    print('\n')

    # Output train, eval, and test to appropriate folders as csv's:
    print('Exporting...')
    train_df.to_csv(f'./data-prep/fda-cancer/output/train/train.csv', index=False)
    eval_df.to_csv(f'./data-prep/fda-cancer/output/eval/eval.csv', index=False)
    test_df.to_csv(f'./data-prep/fda-cancer/output/test/test.csv', index=False)
    shutil.make_archive(f'./data-prep/fda-cancer/datasets/fda_cancer', 'zip', f'./data-prep/fda-cancer/output')

# Main:
main()