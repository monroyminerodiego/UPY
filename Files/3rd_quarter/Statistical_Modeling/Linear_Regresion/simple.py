class simple_linear_regression:
    def __generate_full_matrix(self,basic_matrix:list):
        '''
        Private function to generate a pandas DataFrame with the information and necessary columns to be used as guide to realize the simple linear regression

        Inputs:
        - basic_matrix [list]: Expects a list with 'x' and 'y' values arranged in an iterable object. Eg: [ [1,2],[2,3],...,[6,7] ]

        Outputs:
        - Returns a pandas DataFrame with 4 columns: 'x', 'y', 'x^2' and 'xy'. And their respective value
        '''
        return pd.DataFrame(data={
            "x"   : [value[0]          for value in basic_matrix],
            "y"   : [value[1]          for value in basic_matrix],
            "x^2" : [value[0]**2       for value in basic_matrix],
            "xy"  : [value[0]*value[1] for value in basic_matrix]
        })
    
    def __generate_sumatories(self):
        '''
        Private function to generate the sumatories of the columns of 'full_matrix' DataFrame

        Inputs:
        - Expects nothing

        Outputs:
        - Returns the sumatory values of columns: x, y, xx and xy. (Following that specific order)
        '''
        x  = sum(self.full_matrix["x"])
        y  = sum(self.full_matrix["y"])
        xx = sum(self.full_matrix["x^2"])
        xy = sum(self.full_matrix["xy"])
        return x, y, xx, xy
    
    def __get_relevant_values(self):
        '''
        Private function to get relevant values of the pandas DataFrame, such as: number of observations, slope of the line, intercept and the slope-intercept values.

        Inputs:
        - Expects nothing

        Outputs:
        - Returns n(number of observations), m(slope of the line), b(intercept) and y(slope-intercept) values following that specific order.
        '''
        n = len(self.full_matrix)
        m = ((n*self.sumatory_xy)-(self.sumatory_x*self.sumatory_y))/((n*self.sumatory_xx)-(self.sumatory_x**2))
        b = (self.sumatory_y/n)-(m * (self.sumatory_x/n))
        y = (m * (self.full_matrix["y"].iloc[-1])) + b
        return n,m,b,y
    
    def __get_predictions(self):
        '''
        Private function to calculate the predictions using the minimum square method.

        Inputs:
        - Expects nothing.

        Outputs:
        - Returns bb(sum of the squares of the residuals), m(Error of slope), b(error of intercept) values following that specigic order.
        '''
        bb = sum([pow(row.y - (self.m*row.x+self.b),2) for row in self.full_matrix.itertuples()])
        m  = math.sqrt((self.n/((self.n*self.sumatory_xx)-(self.sumatory_x**2)))*(bb/(self.n-2)))
        b  = math.sqrt((self.sumatory_xx/((self.n*self.sumatory_xx)-(self.sumatory_x**2)))*(bb/(self.n-2)))
        return bb, m, b

    def generate_plot(self):
        '''
        Funtion to plot the scatter plot with the data of 'full_matrix' and it's relevant data.

        Inputs:
        - Expects nothing.

        Outputs:
        - Returns nothing, but generates a window with the plot.
        '''
        x = self.full_matrix['x']
        y = self.full_matrix['y']
        original_line = [self.m * (xi) + self.b for xi in x]
        positive_adjust = [(self.m+self.new_m) * xi + (self.b+self.new_b) for xi in x]
        negative_adjust = [(self.m-self.new_m) * xi + (self.b-self.new_b) for xi in x]
        plt.scatter(x,y)
        plt.grid()
        plt.plot(x,original_line)
        plt.plot(x,positive_adjust)
        plt.plot(x,negative_adjust)
        plt.show()

    def __init__(self,basic_matrix:list):
        '''
        The utility of this class is to make a simple linear regression with its plot

        Inputs:
        - basic_matrix [list]: Expects a list with 'x' and 'y' values arranged in an iterable object. Eg: [ [1,2],[2,3],...,[6,7] ]

        Outputs:
        - Returns nothing but generates the basic structure for a simple linear regression.
        '''
        self.full_matrix = self.__generate_full_matrix(basic_matrix)
        self.sumatory_x ,self.sumatory_y, self.sumatory_xx, self.sumatory_xy = self.__generate_sumatories()
        self.n, self.m, self.b, self.y, = self.__get_relevant_values()
        self.bb, self.new_m, self.new_b = self.__get_predictions()

    def __str__(self):
        string = ''
        string += f"{'*'*10} Data Table {'*'*10}\n\n{self.full_matrix.to_string(index=False)}\n"
        string += f"\nSumatories\nx: {self.sumatory_x}\tx^2: {self.sumatory_xx}\ny: {self.sumatory_y}\txy: {self.sumatory_xy}\n"
        string += f"\n\nUseful Information \nm: {str(self.m)[:6]}\tb: {str(self.b)[:6]}\ny: {str(self.y)[:6]}\tn: {self.n}\n"
        string += f"\n\nLeast Squares\nB^2: {str(self.bb)[:6]}\nNew m: +-{str(self.new_m)[:6]}\nNew b: +-{str(self.new_b)[:6]}"
        return string


if __name__ == '__main__':
    import pandas as pd, os, math, matplotlib.pyplot as plt
    os.system('cls')
    file = pd.read_csv('Databases/simple.csv')
    data = [[row[1],row[2]] for row in file.itertuples()]
    simple_lr = simple_linear_regression(data)
    print(simple_lr)
    simple_lr.generate_plot()