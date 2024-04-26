#-- HOW TO BUILD

The base image contains all dependencies (python 3.11 and autogluon, pandas, etc). The submission image contains a script which executes autogluon training of binary data classifiers, and is configurable.

IMPORTANT: The base image only needs to be built once, whereas the submission image needs to build on each code change or new training test.

1. Build Base:
- cd base
- docker compose up --build
- cd ..

2. Build Wrapper:
- cd submission
- docker compose up --build
- cd ..

#-- WRAPPER DETAILS/INSTRUCTIONS

To change which dataset you want to use for model training job, change the environment variables specified in the docker-compose.yml file to represent the dataset you want to train/predict on

If the dataset you want to use isn't in the "datasets" folder already, zip the folder containing your dataset and place it in the datasets directory. Make sure dataset has following folder structure:
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