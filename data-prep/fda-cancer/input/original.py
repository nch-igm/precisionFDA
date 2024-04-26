import os
import pandas
import shutil
from merge import merge_train, merge_test
from stratification import stratify

# Functions:
def main():

    shutil.make_archive(f'./data-prep/fda-cancer/datasets/fda_brain_cancer_original', 'zip', f'./data-prep/fda-cancer/output')

# Main:
main()