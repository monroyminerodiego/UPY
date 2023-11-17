class Cleaning:

    def __clean_raw_data(self):
        '''
        '''
        # Selecting only 'USA' players        
        df = self.raw_file.query("country == 'USA'")

        # Checking which columns are related to 'net_orating'
        columns_with_needed_correlation = [row.Index for row in self.raw_file.corr().itertuples() if row.net_orating >= self.correlation_in_columns]

        # Adding season to columns
        columns_with_needed_correlation.append('season')

        # Selecting only features that we need from our df
        df = df[columns_with_needed_correlation]

        return df


    def __init__(self, raw_file_path:str, correlation_in_columns:float, cleaned_file_path:str = ''):
        '''
        '''
        # Reading our CSV
        self.raw_file = pd.read_csv(raw_file_path,index_col=0)
        self.correlation_in_columns = correlation_in_columns
        self.df = self.__clean_raw_data()

if __name__ == '__main__':
    import os; os.system('cls')
    import pandas as pd

    input = '../Databases/raw_data.csv'
    correlation = 0.49
    output_path = '../Databases/'
    
    Cleaning(input,correlation,cleaned_file_path=output_path)