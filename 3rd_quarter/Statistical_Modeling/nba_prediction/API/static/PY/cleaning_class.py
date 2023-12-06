import os, pandas as pd, matplotlib.pyplot as plt
from matplotlib import axis
from sklearn.preprocessing import MinMaxScaler, StandardScaler
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

        # Checking which columns are related to 'net_rating'|
        columns_with_needed_correlation = [row.Index for row in df.corr().itertuples() if row.net_rating >= self.correlation_in_columns]
        if self.verbose: print(f"Correlation matrix...\n{df.corr()}",end='\n\n')

        # Selecting only features that we need from our df
        df = df[columns_with_needed_correlation]

        # Validator to drop 'gp' column
        if 'gp' in df.columns: df.drop(axis=1,labels='gp',inplace=True)

        if self.verbose: print(f"Data cleaned...\n{df.corr()}",end='\n\n')
        return df

    def __drop_outliers(self):
        '''
        Private method to eliminate the outliers of the 'clean_data_df'.

        INPUT
        * Expects nothing.

        OUTPUT
        * Returns a 'pandas.DataFrame' with the outliers dropped from 'clean_data_df'.
        '''
        
        df = self.clean_data_df
        for column in df.columns:
            q1, q2, q3 = df[column].quantile([0.25,0.50,0.75])
            interquartile_range = q3 - q1
            upper_limit = q3 + 1.5 * interquartile_range
            lower_limit = q3 - 1.5 * interquartile_range


            df = df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]
        return df

    def __scaler_method(self):
        '''
        Private method to standarize data by scaling method

        INPUT
        - Expects nothing

        OUTPUT
        - Returns a dataframe with the standarized data
        '''
        df = self.clean_data_df
        dependent_variable_list = df[self.dependent_variable_name]
        dependent_variable_list.reset_index(drop=True, inplace=True)
        df = df.drop(labels=[self.dependent_variable_name],axis=1)
        standar_scaler = StandardScaler()
        normalized = standar_scaler.fit_transform(df)
        normalized = pd.DataFrame(data=normalized, columns=df.columns)
        normalized.reset_index(drop=True, inplace=True)

        df = pd.concat((dependent_variable_list,normalized),axis=1)
        return df
    
    def __minmax_method(self):
        '''
        Private method to standarize data by Min-Max method

        INPUT
        - Expects nothing

        OUTPUT
        - Returns a dataframe with the standarized data
        '''
        df = self.clean_data_df
        dependent_variable_list = df[self.dependent_variable_name]
        dependent_variable_list.reset_index(drop=True, inplace=True)
        df = df.drop(labels=[self.dependent_variable_name],axis=1)
        minmax_scaler = MinMaxScaler()
        normalized = minmax_scaler.fit_transform(df)
        normalized = pd.DataFrame(data=normalized, columns=df.columns)
        normalized.reset_index(drop=True, inplace=True)
        df = pd.concat((dependent_variable_list,normalized),axis=1)
        return df

    def __init__(self, raw_file_path:str, dependent_variable_name:str = 'net_rating', correlation_in_columns:float = 0.49, normalization_method:str = 'Scaler', download_mode:bool = False, cleaned_file_path:str = '', verbose:bool = False):
        '''
        Class created to do the cleaning of a CSV file

        INPUT
        - raw_file_path           [str]   = Expects the path where the raw_data is located.
        - dependent_variable_name [str]   = Expects the name of the dependent variable. default set to 'net_rating'.
        - correlation_in_columns  [float] = Expects a value between 0 and 1 that will be used to select columns that fits in that range. Default set to 0.49.
        - normalization_method    [str]   = Refers to the method that will be used to normalize data. Default set to 'Scaler'.
        - download_mode           [bool]  = If set to 'True', then at the end of the cleaning, a CSV file will be stored in 'cleaned_file_path'. Default set to 'False'.
        - cleaned_file_path       [str]   = Expects the path where the 'cleaned_raw_data.csv' file will be located.
        - verbose                 [bool]  = If set to 'True', it will be printing the process of the data cleaning; recommended for debugging. Default set to 'False'.

        OUTPUT (According to method)
        - __init__(download_mode = True) = Downloads a CSV file with the cleaned data.
        - save_distribution_image() = Downloads a PNG image with the distribution of the cleaned data.
        '''
        # Defining parameters
        self.dependent_variable_name = dependent_variable_name
        self.correlation_in_columns = correlation_in_columns
        self.verbose = verbose

        # Reading our CSV
        self.raw_file = pd.read_csv(raw_file_path,index_col=0)
        if verbose: print(f"{'*'*15} Handling Raw Data {'*'*15}\n{self.raw_file.head().to_string()}",end='\n\n')
        self.clean_data_df = self.__clean_raw_data()

        # Dropping outliers
        self.clean_data_df = self.__drop_outliers()
        if verbose: print(f"{'*'*15} DataSet without Outliers {'*'*15}\n{self.clean_data_df.head().to_string()}",end='\n\n')

        # Estandarizing data
        if normalization_method == 'Min-Max':
            self.clean_data_df = self.__minmax_method()
        else:
            self.clean_data_df = self.__scaler_method()
        if verbose: print(f"\n{'*'*15} Scaled DataSet {'*'*15}\n{self.clean_data_df.head().to_string()}",end='\n\n')

        # # Saving document
        if download_mode: 
            self.clean_data_df.to_csv(f'{cleaned_file_path}cleaned_raw_data.csv')
            if verbose: print('\nFile saved...!\n\n')

    def save_distribution_image(self,download_image_path:str):
        '''
        Public method to get a graph with the histogram of every column and save it.

        INPUT
        * Expects nothing

        OUTPUT
        * Returns nothing, but saves an image with the plot in the 'download_image_path'.
        '''
        x = 1
        fig = plt.figure(figsize=(10, 6))
        for column in self.clean_data_df.columns:
            if column == self.dependent_variable_name: continue
            plt.subplot(2,2,x)
            plt.hist(self.clean_data_df[column])
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
        dependent_variable_name = 'net_rating',
        download_mode          = False,
        cleaned_file_path      = '',
        verbose                = True
    ).save_distribution_image('../Images/raw_data_distribution.png')