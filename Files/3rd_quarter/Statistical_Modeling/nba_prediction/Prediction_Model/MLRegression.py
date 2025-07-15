import os
import pandas as pd, math, numpy as np
import random

class MLRegression:
    def __split_dataframe(self,basic_matrix:list):
        '''
        Private method to split the dataframe in order to get the training and testing section in a random way.

        INPUT
        * basic_matrix [list of iterable objects] = Expects a list of iterable objects.

        OUTPUT
        * training_matrix [list of iterble objects] = Returs a list of iterable objects only with the data selected for training.
        * [numpy.Array] = Returns a list of iterable objects only with the data selected for testing.
        '''
        used_index = []
        df = pd.DataFrame(data = basic_matrix, columns=['y','x1','x2','x3','x4'])
        training_matrix = []
        for _ in range(round(self.training_size * len(df))):
            random_index = random.randint(0,len(basic_matrix)-1)
            while random_index in used_index: random_index = random.randint(0,len(basic_matrix)-1)
            training_matrix.append(basic_matrix[random_index])
            df.drop([random_index],axis=0)
            used_index.append(random_index)

        return training_matrix, np.array(df[:])
    
    def __generate_data_table(self,basic_matrix:list):
        '''
        Private method to generate the data table of the dataset for 1 dependent variable and 4 independent variables.

        INPUT
        * basic_matrix [list]: Expects a list of tuples with the independent and dependen variables (y, x1, x2, x3, x4).

        OUTPUT
        * dataframe [pandas.DataFrame]: Returns a pandas dataframe which will be used as the data table.
        '''
        return pd.DataFrame(data={
            'y'    : [ value[0]           for value in basic_matrix],
            'x1'   : [ value[1]           for value in basic_matrix],
            'x2'   : [ value[2]           for value in basic_matrix],
            'x3'   : [ value[3]           for value in basic_matrix],
            'x4'   : [ value[4]           for value in basic_matrix],
            'x1x1' : [ value[1]**2        for value in basic_matrix],
            'x1x2' : [ value[1]*value[2]  for value in basic_matrix],
            'x1x3' : [ value[1]*value[3]  for value in basic_matrix],
            'x1x4' : [ value[1]*value[4]  for value in basic_matrix],
            'x2x2' : [ value[2]**2        for value in basic_matrix],
            'x2x3' : [ value[2]*value[3]  for value in basic_matrix],
            'x2x4' : [ value[2]*value[4]  for value in basic_matrix],
            'x3x3' : [ value[3]*value[3]  for value in basic_matrix],
            'x3x4' : [ value[3]*value[4]  for value in basic_matrix],
            'x4x4' : [ value[4]**2        for value in basic_matrix],
            'x1y'  : [ value[0]*value[1]  for value in basic_matrix],
            'x2y'  : [ value[0]*value[2]  for value in basic_matrix],
            'x3y'  : [ value[0]*value[2]  for value in basic_matrix],
            'x4y'  : [ value[0]*value[2]  for value in basic_matrix],
        })
    
    def __generate_sumatories(self):
        '''
        Private method to generate the sumatories of all columns in the data_table

        INPUT
        * Expects nothing

        OUTPUT
        * Returns a tuple with the values of the summatories of every column
        '''
        y     = sum(self.training_data_table["y"])
        x1    = sum(self.training_data_table["x1"])
        x2    = sum(self.training_data_table["x2"])
        x3    = sum(self.training_data_table["x3"])
        x4    = sum(self.training_data_table["x4"])
        x1x1  = sum(self.training_data_table['x1x1'])
        x1x2  = sum(self.training_data_table['x1x2'])
        x1x3  = sum(self.training_data_table['x1x3'])
        x1x4  = sum(self.training_data_table['x1x4'])
        x2x2  = sum(self.training_data_table['x2x2'])
        x2x3  = sum(self.training_data_table['x2x3'])
        x2x4  = sum(self.training_data_table['x2x4'])
        x3x3  = sum(self.training_data_table['x3x3'])
        x3x4  = sum(self.training_data_table['x3x4'])
        x4x4  = sum(self.training_data_table['x4x4'])
        x1y   = sum(self.training_data_table['x1y'])
        x2y   = sum(self.training_data_table['x2y'])
        x3y   = sum(self.training_data_table['x3y'])
        x4y   = sum(self.training_data_table['x4y'])
        
        return y, x1, x2, x3, x4, x1x1, x2x2, x1x2, x1x3, x1x4, x2x3, x2x4, x3x3, x3x4, x4x4, x1x2, x1y, x2y, x3y, x4y
    
    def __generate_matrix_and_coeficients(self):
        '''
        Private method to generate the matrix, according to the summatories, in orden to know the coefficient that denote the effect of the independent variables on the dependent variable

        INPUT
        * Expects nothing

        OUTPUT
        * Returns a tuple with matrix, the intercept and the coefficients of every independent variable
        '''
        matrix = [
            [len(self.training_data_table),  self.sumatory_x1  ,  self.sumatory_x2  ,  self.sumatory_x3,    self.sumatory_x4  ],
            [self.sumatory_x1    ,  self.sumatory_x1x1,  self.sumatory_x1x2,  self.sumatory_x1x3,  self.sumatory_x1x4],
            [self.sumatory_x2    ,  self.sumatory_x1x2,  self.sumatory_x2x2,  self.sumatory_x2x3,  self.sumatory_x2x4],
            [self.sumatory_x3    ,  self.sumatory_x1x3,  self.sumatory_x2x3,  self.sumatory_x3x3,  self.sumatory_x3x4],
            [self.sumatory_x4    ,  self.sumatory_x1x4,  self.sumatory_x2x4,  self.sumatory_x3x4,  self.sumatory_x4x4],
        ]
        a, b1, b2, b3, b4 = np.linalg.solve(matrix,[self.sumatory_y,self.sumatory_x1y,self.sumatory_x2y,self.sumatory_x3y,self.sumatory_x4y])
        return matrix, a, b1, b2, b3, b4

    def __generate_sum_error_squares(self):
        '''
        Private method to generate 4 columns to 'data_table':{
            p   : Pronostic of dependent variable,
            e   : Error / residue of substracting the pronostic to the dependent variable,
            ee  : Error / residue of substracting the pronostic to the dependent variable multiplied by itself,
            SCR : Sumatory of regression squares
        }

        INPUT
        * Expects nothing

        OUTPUT
        * Returns the sum of the squares errors column (ee).
        '''
        self.training_data_table["p" ]  = [ self.a + (self.b1 * row.x1) + (self.b2 * row.x2) + (self.b3 * row.x3) + (self.b4 * row.x4) for row in self.training_data_table.itertuples()]
        self.training_data_table["e" ]  = [ row.y - row.p                                     for row in self.training_data_table.itertuples()]
        self.training_data_table["ee"]  = [ row.e**2                                          for row in self.training_data_table.itertuples()]
        self.training_data_table["SCR"] = [ (row.p-(self.sumatory_y / self.n))**2             for row in self.training_data_table.itertuples()]
        return sum(self.training_data_table['ee'])

    def __generate_standar_error(self):
        '''
        Private method to generate the standar error following the formula:
        sqrt(sumatory of squares error / Number of rows - ( Number of independent variables + 1)).

        INPUT
        * Expects nothing.
        
        OUTPUT
        * Returns the value of the formula with the correct values.
        '''
        return math.sqrt((self.sumatory_error_squares)/(self.n - (4 + 1))) # 2 number of independent variables

    def __generate_multi_determination_coefficient(self):
        '''
        Private method to generate the sumatory of the residue of substracting the pronostic to the dependent variable multiplied by itself plus the sumatory of regression squares.

        INPUT
        * Expects nothing
        
        OUTPUT
        * Returns the value of the needed summatory
        '''
        return sum(self.training_data_table["ee"]) + sum(self.training_data_table["SCR"])

    def __adjust_multi_determination_coefficient(self):
        '''
        Private method to adjust the multi_determination_coefficient using the formula:
        1 - (1 - multi_determination_coefficient) * ((Number of rows - 1) / (Number of rows - Number of independent variables - 1)).

        INPUT
        * Expects nothing.
        
        OUTPUT
        * Returns the value of the formula with the correct values.
        '''
        return 1 - (1 - self.RR) * ((self.n - 1)/(self.n - 4 - 1)) # 2 number of independent variables

    def __init__(self,basic_list:list,training_size:float = 0.8):
        """
        Class created to do a multiple linear regression of 1 dependent variable and 4 independent variables only.

        INPUT
        * basic_matrix [list of iterable objects]: Expects an iterable object, from 0 to 1, with the information of every row of the dataset.\n
            The iterable object needs to follow (y, x1, x2, x3, x4) format, being{\n
                y              : Dependent variable.\n
                x1, x2, x3, x4 : Independent variables.\n
            }
        * training_size [float]: Expects a float number indicating the percentage of the data set destinated for training. Default is set to '0.8'.
        
        OUTPUT
        * Returns nothing
        """
        self.training_size = training_size
        self.training_list, self.testing_list = self.__split_dataframe(basic_list)
        self.training_data_table = self.__generate_data_table(self.training_list)
        self.n = len(self.training_list)
        self.sumatory_y, self.sumatory_x1, self.sumatory_x2, self.sumatory_x3, self.sumatory_x4, self.sumatory_x1x1, self.sumatory_x2x2, self.sumatory_x1x2, self.sumatory_x1x3, self.sumatory_x1x4, self.sumatory_x2x3, self.sumatory_x2x4, self.sumatory_x3x3, self.sumatory_x3x4, self.sumatory_x4x4, self.sumatory_x1x2, self.sumatory_x1y, self.sumatory_x2y, self.sumatory_x3y, self.sumatory_x4y = self.__generate_sumatories()
        self.matrix, self.a, self.b1, self.b2, self.b3, self.b4 = self.__generate_matrix_and_coeficients()
        self.sumatory_error_squares           = self.__generate_sum_error_squares()
        self.standar_error                    = self.__generate_standar_error()
        self.RR                               = sum(self.training_data_table['SCR']) / self.__generate_multi_determination_coefficient()
        self.RR_adjusted                      = self.__adjust_multi_determination_coefficient()
        self.R                                = math.sqrt(self.RR)

    def __str__(self):
        string  = f"\n{'*'*10} Training Data Table {'*'*10}\n\n{self.training_data_table.head().to_string(index=False)}\n"

        string += f"\n{'*'*10} Summatories {'*'*10}\n\ny: {self.sumatory_y} \t x1: {self.sumatory_x1}\n"
        string += f"x2: {self.sumatory_x2}\t\tx1x1: {self.sumatory_x1x1}\n"
        string += f"x2x2: {self.sumatory_x2x2}\t\tx1x2: {self.sumatory_x1x2}\n"
        string += f"x1y: {self.sumatory_x1y}\t\tx2y: {self.sumatory_x2y}\n"

        string += f"\n{'*'*10} Coeficients {'*'*10}\n\n"
        string += f"a: {self.a}\tb1: {self.b1}\n"
        string += f"b2: {self.b2}\t\tb3: {self.b3}\n"
        string += f"b4: {self.b4}\n"

        # string += f"\nStandar Error of Multiple Estimation: {self.standar_error:02f}\n"

        # string += f"\nError Squares: {self.sumatory_error_squares:02f}"
        string += f"\nMultiple Correlation Coefficient (R2): {self.RR * 100:02f}\n"
        string += f"\nAdjusted Manual R2: {self.RR_adjusted * 100:02f}\n"

        return string

    def predict(self,specific_values:list = []):
        '''
        Public method to do a prediction based on the coefficients.

        INPUT
        * specific_values [list of iterable objects] = Expects a list of iterable objects with (x1,x2,x3,x4) information to make the prediccion.

        OUTPUT
        * Returns a list with the predictions in the same order that came in the input.
        '''
        print('\n\n\n',specific_values,'\n\n\n')
        testing = pd.DataFrame(data={
            "y^" : [self.a+(row[0]*self.b1)+(row[1]*self.b2)+(row[2]*self.b3)+(row[3]*self.b4) for row in specific_values],
            "x1" : [row[0] for row in specific_values],
            "x2" : [row[1] for row in specific_values],
            "x3" : [row[2] for row in specific_values],
            "x4" : [row[3] for row in specific_values]
        })

        return testing['y^'].values

if __name__ == '__main__':
    os.system('cls')

    file = pd.read_csv('C:/Users/diego/OneDrive/PROGRAMACION/UPY/3rd_quarter/Statistical_Modeling/nba_prediction/Databases/cleaned_raw_data.csv')
    data = np.array(file[['net_rating','pts','reb','ast','usg_pct']])
    
    pct_training = 0.8
    
    model = MLRegression(
        basic_list = data, #type:ignore
        training_size = pct_training
    )
    
    prediction_list = [
        [2.9768789776189846,1.0278885699836584,3.4471073863787116,2.842656245134895]
    ]

    print(model.predict(prediction_list),
          model,
          sep='\n\n')
