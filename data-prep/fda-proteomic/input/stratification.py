import pandas
import random

def stratify(split, df, columns=[]):

    row_mapping = {}
    for i in range(len(df)):

        row = df.iloc[i]

        row_id = ''
        for column in columns:
            row_id += str(column) + ':' + str(row[column]) + ':::'
        row_id = row_id[:-3]
        
        if row_mapping.get(row_id):
            row_mapping[row_id].append(i)
        else:
            row_mapping[row_id] = [i]

    group_rows = [[], []]
    for row_id in row_mapping:

        rows = row_mapping[row_id]
        random.shuffle(rows)

        x = round(split * len(rows))
        print('Permutation: ' + str(row_id))
        print('Number of permutations: ' + str(len(rows)))
        print('Number assigned to group 0: ' + str(x))
        print('Number assigned to group 1: ' + str(len(rows) - x))
        print('Desired split ratio: ' + str(split))
        print('Actual split ratio: ' + str(x / len(rows)))
        print('Proportion of total: ' + str(len(rows) / len(df)))
        print('Proportion of group 0 total: ' + str(x / (split * len(df))))
        print('Proportion of group 1 total: ' + str((len(rows) - x) / ((1 - split) * len(df))))
        print('\n')

        for i in range(x):
            group_rows[0].append(rows.pop())
        for row in rows:
            group_rows[1].append(row)

    group_dfs = []
    for group in group_rows:

        df_rows = []
        for i in group:
            df_rows.append(df.iloc[i])
        
        group_df = pandas.DataFrame(df_rows)
        group_df = group_df.sample(frac = 1)
        group_dfs.append(group_df)

    return group_dfs[0], group_dfs[1]