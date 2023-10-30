import pandas as pd, os, math, matplotlib.pyplot as plt 

class simple_linear_regresion:

    def __init__(self,basic_matrix:list):
        '''
        Comentario en constructor
        '''
        self.complex_matrix = pd.DataFrame(data={
            "x"   : [value[0]          for value in basic_matrix],
            "y"   : [value[1]          for value in basic_matrix],
            "x^2" : [value[0]**2       for value in basic_matrix],
            "y^2" : [value[1]**2       for value in basic_matrix],
            "xy"  : [value[0]*value[1] for value in basic_matrix]
        })
        
        self.sumatory_x     = sum(self.complex_matrix["x"])
        self.sumatory_y     = sum(self.complex_matrix["y"])
        self.sumatory_xx    = sum(self.complex_matrix["x^2"])
        self.sumatory_yy    = sum(self.complex_matrix["y^2"])
        self.sumatory_xy    = sum(self.complex_matrix["xy"])

        self.n      = len(basic_matrix)
        self.m      = ((self.n*self.sumatory_xy)-(self.sumatory_x*self.sumatory_y))/((self.n*self.sumatory_xx)-(self.sumatory_x**2))
        self.b      = (self.sumatory_y/self.n)-(self.m * (self.sumatory_x/self.n))
        self.y      = (self.m * (self.complex_matrix["y"].iloc[-1])) + self.b
        
        self.bb = sum([pow(row.y - (self.m*row.x+self.b),2) for row in self.complex_matrix.itertuples()])
        self.new_m  = math.sqrt((self.n/((self.n*self.sumatory_xx)-(self.sumatory_x**2)))*(self.bb/(self.n-2)))
        self.new_b = math.sqrt((self.sumatory_xx/((self.n*self.sumatory_xx)-(self.sumatory_x**2)))*(self.bb/(self.n-2)))

    def generate_plot(self):
        x = self.complex_matrix['x']
        y = self.complex_matrix['y']
        original_line = [self.m * (xi) + self.b for xi in x]
        positive_adjust = [(self.m+self.new_m) * xi + (self.b+self.new_b) for xi in x]
        negative_adjust = [(self.m-self.new_m) * xi + (self.b-self.new_b) for xi in x]
        plt.scatter(x,y)
        plt.grid()
        plt.plot(x,original_line)
        plt.plot(x,positive_adjust)
        plt.plot(x,negative_adjust)
        plt.show()
    
    def __str__(self):
        string = ''
        string += f"{'*'*10} Data Table {'*'*10}\n\n{self.complex_matrix.head().to_string(index=False)}\n"
        string += f"\n\nUseful Information \nm: {str(self.m)[:6]}\tb: {str(self.b)[:6]}\ny: {str(self.y)[:6]}\tn: {self.n}\n"
        string += f"\n\nLeast Squares\nB^2: {str(self.bb)[:6]}\nNew m: +-{str(self.new_m)[:6]}\nNew b: +-{str(self.new_b)[:6]}"
        return string


if __name__ == '__main__':
    os.system('cls')

    file = pd.read_csv('Databases/simple.csv')
    data = [[row[1],row[2]] for row in file.itertuples()]
    simple_lr = simple_linear_regresion(data)
    print(simple_lr)
    simple_lr.generate_plot()