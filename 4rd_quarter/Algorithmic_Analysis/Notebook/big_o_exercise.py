from random import randint

class sort_list_big_o:
    def __init__(self,array:list = [9,1,3,7,5,6,4,8,2,0],target:int = randint(0,9)):
        '''
        '''
        self.array = array
        self.target = target

    def constant_time(self):
        '''
        '''
        first, second = 0, 1
        while True:
            if self.array[first] > self.array[second]:
                pass

        

if __name__ == '__main__':
    '''
    Based on the big O algorithm create an algortihm that could sort a list using the following:
        * O(1): Constant time
        * O(log n): Logarithmic time
        * O(n): Linear time
        * O(n log n): Linearithmic time
        * O(n^2): Quadratic time
    '''
    test = sort_list_big_o()
