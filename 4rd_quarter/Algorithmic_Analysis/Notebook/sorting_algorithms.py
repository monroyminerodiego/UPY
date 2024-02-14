import random
import time


class sorting_algorithms:
    def bubble_sort(self,array:list = [9,1,7,3,8,2,4,5,6,0]) -> list:
        """
        Sorts an array in ascending order using the Bubble Sort algorithm.
        
        ### Args:
        * array (list, optional): A list of elements to be sorted. Default is set to [9,1,7,3,8,2,4,5,6,0].

        ### Returns:
        * array: Sorted array list.
        """
        n = len(array)
        for i in range(n):
            for j in range(0, n-i-1):
                if array[j] > array[j+1]:
                    array[j], array[j+1] = array[j+1], array[j]
        return array

    def merge_sort(self,array:list = [9,1,7,3,8,2,4,5,6,0]) -> list:
        """
        Sorts an array in ascending order using Merge Sort.
        
        ### Args:
        * array (list, optional): A list of elements to be sorted. Default is set to [9,1,7,3,8,2,4,5,6,0].

        ### Returns:
        * array: Sorted array list.
        """
        if len(array) > 1:
            mid = len(array) // 2
            L = array[:mid]
            R = array[mid:]
            self.merge_sort(L)
            self.merge_sort(R)
            i = j = k = 0
            while i < len(L) and j < len(R):
                if L[i] < R[j]:
                    array[k] = L[i]
                    i += 1
                else:
                    array[k] = R[j]
                    j += 1
                k += 1
            while i < len(L):
                array[k] = L[i]
                i += 1
                k += 1
            while j < len(R):
                array[k] = R[j]
                j += 1
                k += 1
        return array

    def quick_sort(self, array:list = [9,1,7,3,8,2,4,5,6,0]) -> list:
        """
        Sorts an array in ascending order using the Quick Sort algorithm.
        
        ### Args:
        * array (list, optional): A list of elements to be sorted. Default's to: [9,1,7,3,8,2,4,5,6,0].

        ### Returns:
        * list: The sorted list.
        """
        if len(array) < 2:
            return array
        else:
            pivot = array[0]
            less = [i for i in array[1:] if i <= pivot]
            greater = [i for i in array[1:] if i > pivot]
            return self.quick_sort(less) + [pivot] + self.quick_sort(greater)

    def linear_search(self,array:list = [9,1,7,3,8,2,4,5,6,0],target:int = 5) -> bool:
        '''
        Searchs for a target using the linear search algorithm.
        
        ### Args:
        * array (list, optional): A list of elements in which the target will be searched. Default's to: [9,1,7,3,8,2,4,5,6,0].
        * target (int, optional): An integer to check if is in the list.

        ### Returns:
        * bool: Indicating if the target was found in the list or not. 
        '''
        for i in range(len(array)):
            if array[i] == target:
                return True
        return False
    
    def binary_search(self,array:list = [9,1,7,3,8,2,4,5,6,0],target:int = 5) -> bool:
        '''
        Searchs for a target using the binary search algorithm.
        
        ### Args:
        * array (list, optional): A list of elements in which the target will be searched. Default's to: [9,1,7,3,8,2,4,5,6,0].
        * target (int, optional): An integer to check if is in the list.

        ### Returns:
        * bool: Indicating if the target was found in the list or not. 
        '''
        low = 0
        high = len(array) - 1
        while low <= high:
            mid = (low + high) // 2
            if array[mid] == target:
                return True
            elif array[mid] < target:
                low = mid + 1
            else:
                high = mid - 1
        return False

    def time_function(self):
        '''
        Measures the time elapsed during the execution of a function.

        ### Args:
        * func (callable): The search/sort function to be measured.

        ### Returns:
        * float: The time elapsed durign the execution of the function.
        '''
        for func in [self.bubble_sort,self.merge_sort,self.quick_sort,self.linear_search,self.binary_search]:
            time_elapsed = time.time()
            print(type(func))
            print(f"Time elapsed during execution of {func.__name__}: {time.time() - time_elapsed}")


if __name__ == '__main__':
    '''
    Part 1: Sorting Algorithms Implementation
        * Bubble Sort Implementation:
            Write a Python function bubble_sort(arr) that implements the Bubble Sort algorithm.
            Test your function with an example array and print the sorted result.
    
        * Merge Sort Implementation:
            Write a Python function merge_sort(arr) that implements the Merge Sort algorithm.
            Test your function with an example array and print the sorted result.
        
        * Quick Sort Implementation:
            Write a Python function quick_sort(arr) that implements the Quick Sort algorithm.
            Test your function with an example array and print the sorted result.

    Part 2: Searching Algorithms Implementation
        * Linear Search Implementation:
            Write a Python function linear_search(arr, target) that implements the Linear Search algorithm.
            Test your function with an example array and print whether the target is found or not.

        * Binary Search Implementation:
            Write a Python function binary_search(arr, target) that implements the Binary Search algorithm.
            Test your function with a sorted example array and print whether the target is found or not.

    Part 3: Time Complexity Analysis
        * Analyze Time Complexity:
            For each sorting and searching function implemented in Parts 1 and 2, analyze the time complexity in terms of Big O notation.
            Provide a brief written explanation for each analysis.

        * Evaluate and Compare:
            Create an array of size 1000 with random integers and apply each sorting algorithm. Measure the execution time for each.
            Use Big O notation to compare the expected and observed time complexities of the sorting algorithms.

    Submission Instructions:
        * Submit a Python script file containing your implementations (sorting_algorithms.py).
        * Include a separate text document (analysis.txt) with your time complexity analysis and comparison results.
    '''

    test = sorting_algorithms()

    test.time_function()