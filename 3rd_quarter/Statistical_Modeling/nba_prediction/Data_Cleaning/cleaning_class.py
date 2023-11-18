class Cleaning:

    def __clean_raw_data(self):
        '''
        Private method to make the cleaning of the raw_data_file

        Inputs
        - Excepts nothing

        Output
        - Returns a pandas.DataFrame with the cleaned data
        '''
        # Selecting only 'USA' players        
        df = self.raw_file.query("country == 'USA'")

        # Checking which columns are related to 'net_orating'
        columns_with_needed_correlation = [row.Index for row in self.raw_file.corr().itertuples() if row.net_orating >= self.correlation_in_columns]

        # Adding season to columns
        columns_with_needed_correlation.append('season')

        # Selecting only features that we need from our df
        df = df[columns_with_needed_correlation]

        # Creating the dictionary to map the categorical data
        dict_season = {}
        counter = 1
        for i in sorted(set(df['season'])):
            dict_season[i] = counter
            counter += 1

        # Changing to categorical the 'season' feature
        df['season'] = df['season'].apply(lambda x: dict_season[x])

        return df

    def __estandarizing_data(self):
        '''
        Private method to standarize data

        Input
        - Expects nothing

        Output
        - Returns a dataframe with the standarized data
        '''
        df = self.df
        scaler = StandardScaler()
        df = scaler.fit_transform(df)
        df = pd.DataFrame(df,columns=list(self.df.columns))
        return df

    def __init__(self, raw_file_path:str, correlation_in_columns:float, download_mode:bool = False, cleaned_file_path:str = ''):
        '''
        Class created to do the cleaning of a CSV file

        Input
        - raw_file_path          [str]   : Expects the path where the raw_data is located.
        - correlation_in_columns [float] : Expects a value between 0 and 1 that will be used to select columns that fits in that range.
        - download_mode          [bool]  : If set to True, then at the end of the cleaning, a CSV file will be stored in 'cleaned_file_path'
        - cleaned_file_path      [str]   : Expects the path where the cleaned_data will be located.

        Output
        - Returns nothing, but when 'download_mode' is set to True, then it downloads a CSV File
        '''
        # Defining parameters
        self.correlation_in_columns = correlation_in_columns

        # Reading our CSV
        self.raw_file = pd.read_csv(raw_file_path,index_col=0)
        self.df = self.__clean_raw_data()

        # Estandarizing data
        self.normalized_data = self.__estandarizing_data()

        # Saving document
        if download_mode:
            self.normalized_data.to_csv(f'{cleaned_file_path}cleaned_raw_data.csv')


if __name__ == '__main__':
    import os; os.system('cls')
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    input = '../Databases/raw_data.csv'
    correlation = 0.49
    output_path = '../Databases/'
    
    Cleaning(raw_file_path = input,
             correlation_in_columns = correlation,
             cleaned_file_path=output_path,
             download_mode=True
             )