import pandas as pd
import os

class simple_linear_regresion:
    def __init__(self,basic_matrix:list):
        '''
        Comentario en constructor
        '''
        self.complex_matrix = [[row[0],row[1],row[0]*row[0],row[1]*row[1],row[0]*row[1]] for row in basic_matrix]
        
        self.sumatory_x     = sum([row[0] for row in self.complex_matrix])
        self.sumatory_y     = sum([row[1] for row in self.complex_matrix])
        self.sum_sqr_x      = sum([row[2] for row in self.complex_matrix])
        self.sum_sqr_y      = sum([row[3] for row in self.complex_matrix])
        self.sumaroty_xy    = sum([row[4] for row in self.complex_matrix])

        self.n              = len(basic_matrix)

        
        

    def __str__(self):
        return str(self.complex_matrix)


if __name__ == '__main__':
    os.system('cls')

    file = pd.read_csv('Databases/simple.csv')
    data = [[row[1],row[2]] for row in file.itertuples()]
    simple_lr = simple_linear_regresion(data)
    print(f"{'*'*15} Head of File {'*'*15}\n{file.head()}\n\n{data}\n\n{simple_lr}")
