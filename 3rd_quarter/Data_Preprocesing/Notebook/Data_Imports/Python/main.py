import pandas as pd

file = pd.read_csv(open('../../../DataBases/data_imports.csv','r'))
print(file.describe())