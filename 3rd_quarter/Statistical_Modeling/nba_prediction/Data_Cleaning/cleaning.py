import os; os.system('cls')
import pandas as pd

csv = pd.read_csv('c:/Users/diego/Downloads/diabetes_prediction_dataset.csv')
print(csv.corr())