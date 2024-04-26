import pandas
import random

def under_sample_random(keep, value, df, column):

    row_mapping = {}
    for i in range(len(df)):

        row = df.iloc[i]

        row_id = ''
        row_id += str(column) + ':' + str(row[column]) + ':::'
        row_id = row_id[:-3]
        
        if row_mapping.get(row_id):
            row_mapping[row_id].append(i)
        else:
            row_mapping[row_id] = [i]

    df_row_indexes = []
    for row_id in row_mapping:

        rows = row_mapping[row_id]
        random.shuffle(rows)

        x = round(keep * len(rows)) if row_id[-1] == str(value) else len(rows)

        print('Permutation: ' + str(row_id))
        print('Number of permutations: ' + str(len(rows)))
        print('Number being kept: ' + str(x))
        print('Number being dropped: ' + str(len(rows) - x))

        for i in range(x):
            df_row_indexes.append(rows.pop())

    df_rows = []
    for i in df_row_indexes:
        df_rows.append(df.iloc[i])

    new_df = pandas.DataFrame(df_rows)
    new_df = new_df.sample(frac = 1)

    return new_df

def under_sample_stat(keep_percentage, desired_value, target_column, strat_columns, df):

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
    
