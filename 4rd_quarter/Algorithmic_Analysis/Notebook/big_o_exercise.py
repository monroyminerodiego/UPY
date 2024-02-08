import os
from random import randint

class sort_list_big_o:
    def __init__(self,array:list = [9,1,3,7,5,6,4,8,2,0]):
        '''
        Initializes an instance of the `sort_list_big_o` class.

        This class is designed for performing sorting operations and finding the maximum number in an array. It provides methods with different time complexities for these operations.

        ### Args:
        * `array`: A list of integers to be sorted or searched. Default is `[9, 1, 3, 7, 5, 6, 4, 8, 2, 0]`.

        ### Methods:
        - `sort_by_constant_time`: Sorts an array using a recursive approach with time complexity ranging from `O(N log N)` to `O(N^2)`.
        - `get_max_number`: Finds the maximum number in an array with a time complexity of `O(N)`.

        The instance stores the provided array and is used by these methods for sorting and finding the maximum number.
        '''
        self.array = array
        print(f'Initialized class with array: \n{self.array}')

    # ================== METHOD'S ==================
    def sort_by_constant_time(self,array:list,first:int = 0,second:int = 1):
        '''
        Sorts an array using a recursive approach.

        ### Args:
        * `array`: The list to be sorted.
        * `first`: The index of the first element to compare (default: 0).
        * `second`: The index of the second element to compare (default: 1).

        ### Returns:
        - The sorted `array`.

        ### Time complexity:
        - `O(N^2)` worst-case, `O(N log N)` average-case.
        '''
        while True:
            if array[first] > array[second]:
                # Saves the original values
                left = array[second]
                right = array[first]
                # Rewrites with the correct order
                array[second] = right
                array[first] = left

                array = self.sort_by_constant_time(
                    array  = array
                    )
            else:
                if second+1 == len(array):
                    break
                array = self.sort_by_constant_time(
                    array  = array,
                    first  = first  + 1,
                    second = second + 1
                    )
            break
        return array
    
    def get_max_number(self,array:list):
        '''
        Finds the maximum number in an array.

        ### Args:
        * `array`: The list of numbers to search.

        ### Returns:
        * The maximum number in the `array`.

        ### Time complexity:
        * `O(N)`
        '''
        max_number = 0
        for index in range(len((array))):
            if max_number < array[index]: max_number = array[index]
        return max_number


        

if __name__ == '__main__':
    '''
    Based on the big O algorithm create an algortihm that could sort a list using the following:
        * O(1): Constant time
        * O(log n): Logarithmic time
        * O(n): Linear time
        * O(n log n): Linearithmic time
        * O(n^2): Quadratic time
    '''
    os.system('cls')
    test = sort_list_big_o(
        # array = [4, 2, 7, 1, 9,6]
        # array = [1, 2, 4, 3, 5, 7, 6,8]
    )

    sorted_list = test.sort_by_constant_time(test.array)

    get_max_number = test.get_max_number(test.array)

    print(f"\nThe sorted list is {sorted_list} and the max number is {get_max_number}")