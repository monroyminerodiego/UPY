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
        # Selecting only 'USA' players        
        df = self.raw_file.query("country == 'USA'")

        # Checking which columns are related to 'net_rating'
        columns_with_needed_correlation = [row.Index for row in self.raw_file.corr().itertuples() if row.net_rating >= self.correlation_in_columns]

        # Adding season to columns
        # columns_with_needed_correlation.append('season')

        # Selecting only features that we need from our df
        df = df[columns_with_needed_correlation]

        if 'gp' in df.columns: df.drop(axis=1,labels='gp',inplace=True)

        # Creating the dictionary to map the categorical data
        # dict_season = {}
        # counter = 1
        # for i in sorted(set(df['season'])):
        #     dict_season[i] = counter
        #     counter += 1

        # # Changing to categorical the 'season' feature
        # df['season'] = df['season'].apply(lambda x: dict_season[x])

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

    def __init__(self, raw_file_path:str, correlation_in_columns:float, download_mode:bool = False, cleaned_file_path:str = '', estandarize_data:bool = True, normalize_data:bool = False):
        '''
        Class created to do the cleaning of a CSV file

        INPUT
        - raw_file_path          [str]   : Expects the path where the raw_data is located.
        - correlation_in_columns [float] : Expects a value between 0 and 1 that will be used to select columns that fits in that range.
        - download_mode          [bool]  : If set to 'True', then at the end of the cleaning, a CSV file will be stored in 'cleaned_file_path'. Default set to 'False'
        - cleaned_file_path      [str]   : Expects the path where the cleaned_data will be located.
        - estandarize_data       [bool]  : If set to 'True', the raw data will be estandarized. Default set to 'True'
        - normalize_data         [bool]  : If set to 'True', the raw data will be normalized. Default set to 'False'

        OUTPUT
        - Returns nothing, but when 'download_mode' is set to True, then it downloads a CSV File
        '''
        # Defining parameters
        self.correlation_in_columns = correlation_in_columns

        # Reading our CSV
        self.raw_file = pd.read_csv(raw_file_path,index_col=0)
        self.df = self.__clean_raw_data()

        # Estandarizing data
        if estandarize_data: self.df = self.__estandarizing_data()

        # Normalizing data
        if normalize_data: self.df = self.__normalizing_data()

        # # Saving document
        if download_mode: self.df.to_csv(f'{cleaned_file_path}cleaned_raw_data.csv')

    def save_distribution_image(self,download_image_path:str):
        '''
        Public method to get a graph with the histogram of every column and save it.

        INPUT
        * name_image [str] = Expects the name with extension for the image.
        * download_image_path [str] = Expects the path to download the image.

        OUTPUT
        * Returns nothing, but saves an image with the plot.
        '''
        x = 1
        for column in self.df.columns:
            plt.subplot(round(len(self.df.columns)/3)+1 if len(self.df.columns)%3 != 0 else len(self.df.columns)/3,3,x)
            plt.hist(self.df[column])
            plt.title(column)
            x += 1
        plt.savefig(download_image_path)