import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import normalize

class Cleaning:

    def __clean_raw_data(self):
        '''
        Private method to make the cleaning of the raw_data_file. First it only selects the 'USA' players and then it selects the columns that match with the selected correlation.

        INPUT
        - Excepts nothing

        OUTPUT
        - Returns a pandas.DataFrame with the cleaned data
        '''
        # Selecting only 'USA' players and selecting only columns that can be described.    
        df = self.raw_file.query("country == 'USA'")
        if self.verbose: print(f"Dataset with only 'USA' players...\n{df.head().to_string()}",end='\n\n')

        df = df[[column for column in self.raw_file.describe().columns]]
        if self.verbose: print(f"Dataset with only useful columns...\n{df.head().to_string()}",end='\n\n')

        # Checking which columns are related to 'net_rating'
        columns_with_needed_correlation = [row.Index for row in df.corr().itertuples() if row.net_rating >= self.correlation_in_columns]
        if self.verbose: print(f"Correlation matrix...\n{df.corr()}",end='\n\n')

        # Selecting only features that we need from our df
        df = df[columns_with_needed_correlation]
        if self.verbose: print(f"Data cleaned...\n{df.corr()}",end='\n\n')

        # Validator to drop 'gp' column
        if 'gp' in df.columns: df.drop(axis=1,labels='gp',inplace=True)

        return df

    def __estandarizing_data(self):
        '''
        Private method to standarize data

        INPUT
        - Expects nothing

        OUTPUT
        - Returns a dataframe with the standarized data
        '''
        df = self.df
        scaler = StandardScaler()
        df = scaler.fit_transform(df)
        df = pd.DataFrame(df,columns=list(self.df.columns))
        # df['season'] = self.df['season']
        return df

    def __normalizing_data(self):
        '''
        Private method that normalice data.

        INPUT
        * Expects nothing.

        OUTPUT
        * Returns a pandas.DataFrame with the data normalized.
        '''
        return pd.DataFrame(data=normalize(self.df, axis=0),columns=[column for column in self.df.columns]) #type:ignore

    def __init__(self, raw_file_path:str, correlation_in_columns:float, download_mode:bool = False, cleaned_file_path:str = '', estandarize_data:bool = True, normalize_data:bool = False, verbose:bool = False):
        '''
        Class created to do the cleaning of a CSV file

        INPUT
        - raw_file_path          [str]   = Expects the path where the raw_data is located.
        - correlation_in_columns [float] = Expects a value between 0 and 1 that will be used to select columns that fits in that range.
        - download_mode          [bool]  = If set to 'True', then at the end of the cleaning, a CSV file will be stored in 'cleaned_file_path'. Default set to 'False'
        - cleaned_file_path      [str]   = Expects the path where the 'cleaned_raw_data.csv' file will be located.
        - estandarize_data       [bool]  = If set to 'True', the raw data will be estandarized. Default set to 'True'
        - normalize_data         [bool]  = If set to 'True', the raw data will be normalized. Default set to 'False'
        - verbose                [bool]  = If set to 'True', it will be printing the process of the data cleaning; recommended for debugging. Default set to 'False'

        OUTPUT (According to method)
        - __init__(download_mode = True) = Downloads a CSV file with the cleaned data.
        - save_distribution_image() = Downloads a PNG image with the distribution of the cleaned data.
        '''
        # Defining parameters
        self.correlation_in_columns = correlation_in_columns
        self.verbose = verbose

        # Reading our CSV
        self.raw_file = pd.read_csv(raw_file_path,index_col=0)
        if verbose: print(f"{'*'*15} Handling Raw Data {'*'*15}\n{self.raw_file.head().to_string()}",end='\n\n')
        self.df = self.__clean_raw_data()

        # Estandarizing data
        if estandarize_data: 
            self.df = self.__estandarizing_data()
            if verbose: print(f"\n{'*'*15} Estandarized DataSet {'*'*15}\n{self.df.head().to_string()}",end='\n\n')

        # Normalizing data
        if normalize_data: 
            self.df = self.__normalizing_data()
            if verbose: print(f"\n{'*'*15} Normalized DataSet {'*'*15}\n{self.df.head().to_string()}",end='\n\n')

        # # Saving document
        if download_mode: 
            self.df.to_csv(f'{cleaned_file_path}cleaned_raw_data.csv')
            if verbose: print('\nFile saved...!\n\n')

    def save_distribution_image(self,download_image_path:str,name_dependent_variable:str):
        '''
        Public method to get a graph with the histogram of every column and save it.

        INPUT
        * download_image_path [str] = Expects the path to download the image.
        * name_dependent_variable [str] = Expects the name of the dependent variable.

        OUTPUT
        * Returns nothing, but saves an image with the plot in the 'download_image_path'.
        '''
        x = 1
        fig = plt.figure(figsize=(10, 6))
        for column in self.df.columns:
            if column == name_dependent_variable: continue
            plt.subplot(2,2,x)
            plt.hist(self.df[column])
            plt.title(column)
            x += 1
        fig.tight_layout()
        plt.savefig(download_image_path)


# For debugging
if __name__ == '__main__':
    os.system('cls')
    Cleaning(
        raw_file_path          = '../Downloads/raw_data.csv',
        correlation_in_columns = 0.49,
        download_mode          = False,
        cleaned_file_path      = '',
        estandarize_data       = True,
        normalize_data         = False,
        verbose                = False
    ).save_distribution_image('../Images/raw_data_distribution.png','net_rating')