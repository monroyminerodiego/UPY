class multiple_linear_regression:
    def __generate_data_table(self,basic_matrix:list):
        '''
        Private method to generate the data table of the dataset for 1 dependent variable and 4 independent variables.

        INPUT
        * basic_matrix -> list: Expects a list of tuples with the independent and dependen variables (y, x1, x2, x3, x4).

        OUTPUT
        * dataframe -> pandas.DataFrame: Returns a pandas dataframe which will be used as the data table.
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
        y     = sum(self.data_table["y"])
        x1    = sum(self.data_table["x1"])
        x2    = sum(self.data_table["x2"])
        x3    = sum(self.data_table["x3"])
        x4    = sum(self.data_table["x4"])
        x1x1  = sum(self.data_table['x1x1'])
        x1x2  = sum(self.data_table['x1x2'])
        x1x3  = sum(self.data_table['x1x3'])
        x1x4  = sum(self.data_table['x1x4'])
        x2x2  = sum(self.data_table['x2x2'])
        x2x3  = sum(self.data_table['x2x3'])
        x2x4  = sum(self.data_table['x2x4'])
        x3x3  = sum(self.data_table['x3x3'])
        x3x4  = sum(self.data_table['x3x4'])
        x4x4  = sum(self.data_table['x4x4'])
        x1y   = sum(self.data_table['x1y'])
        x2y   = sum(self.data_table['x2y'])
        x3y   = sum(self.data_table['x3y'])
        x4y   = sum(self.data_table['x4y'])
        
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
            [len(self.data_table),  self.sumatory_x1  ,  self.sumatory_x2  ,  self.sumatory_x3,    self.sumatory_x4  ],
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
        self.data_table["p" ]  = [ self.a + (self.b1 * row.x1) + (self.b2 * row.x2) + (self.b3 * row.x3) + (self.b4 * row.x4) for row in self.data_table.itertuples()]
        self.data_table["e" ]  = [ row.y - row.p                                     for row in self.data_table.itertuples()]
        self.data_table["ee"]  = [ row.e**2                                          for row in self.data_table.itertuples()]
        self.data_table["SCR"] = [ (row.p-(self.sumatory_y / self.n))**2             for row in self.data_table.itertuples()]
        return sum(self.data_table['ee'])

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
        return sum(self.data_table["ee"]) + sum(self.data_table["SCR"])

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

    def __init__(self,basic_matrix:list):
        '''
        Class created to do a multiple linear regression of 1 dependent variable and 4 independent variables.

        INPUT
        * Expects a list of tuples|lists with the information of every row of the dataset.
        The tuple|list needs to follow (y, x1, x2, x3, x4) format, being{
            y              : Dependent variable
            x1, x2, x3, x4 : Independent variables
        }
        
        OUTPUT
        * Returns nothing
        '''
        self.data_table = self.__generate_data_table(basic_matrix)
        self.n = len(basic_matrix)
        self.sumatory_y, self.sumatory_x1, self.sumatory_x2, self.sumatory_x3, self.sumatory_x4, self.sumatory_x1x1, self.sumatory_x2x2, self.sumatory_x1x2, self.sumatory_x1x3, self.sumatory_x1x4, self.sumatory_x2x3, self.sumatory_x2x4, self.sumatory_x3x3, self.sumatory_x3x4, self.sumatory_x4x4, self.sumatory_x1x2, self.sumatory_x1y, self.sumatory_x2y, self.sumatory_x3y, self.sumatory_x4y = self.__generate_sumatories()
        self.matrix, self.a, self.b1, self.b2, self.b3, self.b4 = self.__generate_matrix_and_coeficients()
        self.sumatory_error_squares           = self.__generate_sum_error_squares()
        self.standar_error                    = self.__generate_standar_error()
        self.RR                               = sum(self.data_table['SCR']) / self.__generate_multi_determination_coefficient()
        self.RR_adjusted                      = self.__adjust_multi_determination_coefficient()
        self.R                                = math.sqrt(self.RR)
        
        # Esto es el R2 calculado con sklearn.metrics.r2_score
        self.R2                               = r2_score(self.data_table['y'],self.data_table['p'])

    def __str__(self):
        string  = f"\n{'*'*10} Data Table {'*'*10}\n\n{self.data_table.head().to_string(index=False)}\n"

        string += f"\n{'*'*10} Summatories {'*'*10}\n\ny: {self.sumatory_y} \t x1: {self.sumatory_x1}\n"
        string += f"x2: {self.sumatory_x2} \t\t x1x1: {self.sumatory_x1x1}\n"
        string += f"x2x2: {self.sumatory_x2x2} \t x1x2: {self.sumatory_x1x2}\n"
        string += f"x1y: {self.sumatory_x1y} \t x2y: {self.sumatory_x2y}\n"

        string += f"\n{'*'*10} Coeficients {'*'*10}\n\na: {self.a:02f}\tb1: {self.b1:02f}\nb2: {self.b2:02f}\n"

        string += f"\nStandar Error of Multiple Estimation: {self.standar_error:02f}\n"

        string += f"\nError Squares: {self.sumatory_error_squares:02f}"
        string += f"\nManual R2: {self.RR * 100:02f}"
        string += f"\nAdjusted Manual R2: {self.RR_adjusted * 100:02f}\n"

        string += f"\nMultiple Correlation Coefficient (R): {self.R * 100:02f}\n"

        string += f"\nR2 with sklearn.metrics: {self.R2 * 100:02f}\n"

        return string


if __name__ == '__main__':
    import pandas as pd, os, math, matplotlib.pyplot as plt, numpy as np
    from sklearn.metrics import r2_score
    os.system('cls')
    # file = pd.read_csv('Databases/multiple.csv')
    file = pd.read_csv('../nba_prediction/Databases/cleaned_raw_data_o.csv')
    data = [(row.net_rating,row.pts,row.reb,row.ast,row.usg_pct) for row in file.itertuples()]
    multiple = multiple_linear_regression(data)
