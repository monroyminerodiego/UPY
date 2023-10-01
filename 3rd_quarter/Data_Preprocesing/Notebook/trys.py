import pandas as pd, os, numpy as np
os.system('cls')

# Load Data
df = pd.read_csv('../DataBases/ModalidadVirtual.csv',delimiter=',')

# Delete features with more than 70% missing values
headers_list = df.columns.tolist()
for header in headers_list:
    feature = df[header]
    len_feature = len(feature)
    num_missing_features = (feature.isnull()).sum()
    percentage_missing_features = (num_missing_features * 100) / len_feature
    if percentage_missing_features >= 70: df = df.drop(header,axis=1)

# Delete observations with more than 50% missing values
len_df = len(df)
for row in range(len_df):
    observation = df.loc[row]
    len_observation = len(observation)
    num_missing_observations = (observation.isnull()).sum()
    percentage_missing_observations = (num_missing_observations * 100) / len_observation
    if percentage_missing_observations >= 50: df = df.drop([row], axis=0)

# Check for duplicated rows
duplicated_row_list = []
iteration_index = 0
for row in df.duplicated():
    if row: duplicated_row_list.append(iteration_index)
    iteration_index += 1
df = df.drop(duplicated_row_list, axis=0)

# Delete features with Average = 0
for header in headers_list:
    possible_value_list = []
    feature = df[header]
    for observation in feature:
        if not(observation in possible_value_list): possible_value_list.append(observation)
    if len(possible_value_list) == len(feature): continue
    average = 0
    for value in possible_value_list: average += (df[header] == value).sum()
    average /= len(possible_value_list)
    if average == 0: df = df.drop(header,axis=1)

# Identify type of data of each feature
# for header in headers_list:
    # print(f'{df[header].info()}\n\n{"*"*50}')


# Validate that numbers are numeric Values
for header in headers_list:
    int_count = 0
    float_count = 0
    other_count = 0
    feature = df[header]
    for observation in feature:
        if (type(observation) == int) or (type(observation) == float): 
            int_count += 1 if type(observation) == int else 0
            float_count += 1 if type(observation) == float else 0
        else: other_count += 1
    if not((int_count+float_count) > other_count): continue
    if int_count > float_count:
        df[header] = df[header].astype('int64')
    if float_count > int_count:
        df[header] = df[header].astype('float')


# Identify categorical features → Generate dummies
# print(f'\n\n{"*"*50} Dummies {"*"*50}')
# for header in headers_list:
#     print(f'{pd.get_dummies(df,columns=[header])}')