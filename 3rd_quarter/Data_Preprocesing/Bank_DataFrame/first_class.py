import pandas as pd, os
os.system('cls')

bank_df = pd.read_csv('bank-full.csv',sep=';')
print(bank_df.head(5))
print(bank_df.describe())