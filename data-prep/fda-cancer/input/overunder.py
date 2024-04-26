import pandas
import random
from stratification import stratify

def under_sample(keep_percentage, desired_value, target_column, strat_columns, df):

    retain_rows = []
    reduce_rows = []
    for i in range(len(df)):

        row = df.iloc[i]
        val = str(row[target_column])
        
        if val == str(desired_value):
            reduce_rows.append(row)
        else:
            retain_rows.append(row)

    print('Retaining ' + str(len(retain_rows)) + ' rows.')
    print('Reducing ' + str(len(reduce_rows)) + ' rows.')

    retain_df = pandas.DataFrame(retain_rows)
    reduce_df = pandas.DataFrame(reduce_rows)
    strat_df, _ = stratify(keep_percentage, reduce_df, strat_columns)

    print('Reduced to ' + str(len(strat_df)) + ' rows')

    new_df = pandas.concat([retain_df, strat_df])
    new_df = new_df.sample(frac = 1)

    print('Final row count ' + str(len(new_df)) + ' rows')

    return new_df
    