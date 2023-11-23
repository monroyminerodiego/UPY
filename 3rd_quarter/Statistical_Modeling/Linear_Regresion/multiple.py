class multiple_linear_regression:
    def __generate_data_table(self,basic_matrix:list):
        '''
        '''
        return pd.DataFrame(data={
            "y"    : [value[0]           for value in basic_matrix],
            "x1"   : [value[1]           for value in basic_matrix],
            "x2"   : [value[2]           for value in basic_matrix],
            "x1x1" : [value[1]**2        for value in basic_matrix],
            "x2x2" : [value[2]**2        for value in basic_matrix],
            "x1x2" : [value[1]*value[2]  for value in basic_matrix],
            "x1y"  : [value[0]*value[1]  for value in basic_matrix],
            "x2y"  : [value[0]*value[2]  for value in basic_matrix],
        })
    
    def __generate_sumatories(self):
        '''
        '''
        y     = sum(self.data_table["y"])

        x1    = sum(self.data_table["x1"])
        x2    = sum(self.data_table["x2"])

        x1x1  = sum(self.data_table["x1x1"])
        x2x2  = sum(self.data_table["x2x2"])

        x1x2  = sum(self.data_table["x1x2"])

        x1y   = sum(self.data_table["x1y"])
        x2y   = sum(self.data_table["x2y"])
        
        return y, x1, x2, x1x1, x2x2, x1x2, x1y, x2y
    
    def __generate_matrix_and_coeficients(self):
        '''
        '''
        matrix = [
            [len(self.data_table),self.sumatory_x1,self.sumatory_x2],
            [self.sumatory_x1,self.sumatory_x1x1,self.sumatory_x1x2],
            [self.sumatory_x2,self.sumatory_x1x2,self.sumatory_x2x2]
        ]
        a, b1, b2 = np.linalg.solve(matrix,[self.sumatory_y,self.sumatory_x1y,self.sumatory_x2y])
        return matrix, a, b1, b2

    def __generate_sum_error_squares(self):
        '''
        '''
        self.data_table["p" ]  = [ self.a + (self.b1 * row.x1) + (self.b2 * row.x2)  for row in self.data_table.itertuples()]
        self.data_table["e" ]  = [ row.y - row.p                                     for row in self.data_table.itertuples()]
        self.data_table["ee"]  = [ row.e**2                                          for row in self.data_table.itertuples()]
        self.data_table["SCR"] = [ (row.p-(self.sumatory_y / self.n))**2             for row in self.data_table.itertuples()]
        return sum(self.data_table['ee'])

    def __generate_standar_error(self):
        '''
        '''
        return math.sqrt((self.sumatory_error_squares)/(self.n - (2 + 1))) # 2 number of independent variables

    def __generate_multi_determination_coefficient(self):
        '''
        '''
        return sum(self.data_table["ee"]) + sum(self.data_table["SCR"])

    def __adjust_multi_determination_coefficient(self):
        '''
        '''
        return 1 - (1 - self.RR) * ((self.n - 1)/(self.n - 2 - 1)) # 2 porque es el numero de variables independientes

    def __init__(self,basic_matrix:list):
        '''
        '''
        self.data_table = self.__generate_data_table(basic_matrix)
        self.n = len(basic_matrix)
        self.sumatory_y, self.sumatory_x1, self.sumatory_x2, self.sumatory_x1x1, self.sumatory_x2x2, self.sumatory_x1x2, self.sumatory_x1y, self.sumatory_x2y = self.__generate_sumatories()
        self.matrix, self.a, self.b1, self.b2 = self.__generate_matrix_and_coeficients()
        self.sumatory_error_squares           = self.__generate_sum_error_squares()
        self.standar_error                    = self.__generate_standar_error()
        self.RR                               = sum(self.data_table['SCR']) / self.__generate_multi_determination_coefficient()
        self.RR_adjusted                      = self.__adjust_multi_determination_coefficient()
        self.R                                = math.sqrt(self.RR)
        self.R2                               = r2_score(self.data_table['y'],self.data_table['p'])

    def __str__(self):
        string  = f"\n{'*'*10} Data Table {'*'*10}\n\n{self.data_table.head().to_string(index=False)}\n"

        string += f"\n{'*'*10} Summatories {'*'*10}\n\ny: {self.sumatory_y} \t x1: {self.sumatory_x1}\n"
        string += f"x2: {self.sumatory_x2} \t\t x1x1: {self.sumatory_x1x1}\n"
        string += f"x2x2: {self.sumatory_x2x2} \t x1x2: {self.sumatory_x1x2}\n"
        string += f"x1y: {self.sumatory_x1y} \t x2y: {self.sumatory_x2y}\n"

        string += f"\n{'*'*10} Coeficients {'*'*10}\n\na: {self.a:02f}\tb1: {self.b1:02f}\nb2: {self.b2:02f}\n"

        string += f"\nStandar Error of Multiple Estimation: {self.standar_error:02f}"
        string += f"\nError Squares: {self.sumatory_error_squares:02f}"
        string += f"\nSum all Error Squares: {self.RR * 100:02f}"
        string += f"\nSum all Error Squares Adjusted: {self.RR_adjusted * 100:02f}"

        string += f"\nMultiple Correlation Coefficient: {self.R * 100:02f}"

        string += f"\nR2: {self.R2 * 100:02f}"

        return string
    
    def generate_plot(self):
        '''
        '''
        x = self.data_table['x']
        y = self.data_table['y']
        original_line = [self.m * (xi) + self.b for xi in x]
        positive_adjust = [(self.m+self.new_m) * xi + (self.b+self.new_b) for xi in x]
        negative_adjust = [(self.m-self.new_m) * xi + (self.b-self.new_b) for xi in x]
        plt.scatter(x,y)
        plt.grid()
        plt.plot(x,original_line)
        plt.plot(x,positive_adjust)
        plt.plot(x,negative_adjust)
        plt.show()


if __name__ == '__main__':
    import pandas as pd, os, math, matplotlib.pyplot as plt, numpy as np
    from sklearn.metrics import r2_score
    os.system('cls')
    # file = pd.read_csv('Databases/multiple.csv')
    file = pd.read_csv('../nba_prediction/Databases/cleaned_raw_data.csv')
    data = [(row.net_orating,row.pts,row.ast) for row in file.itertuples()]
    multiple = multiple_linear_regression(data)
    print(multiple)
