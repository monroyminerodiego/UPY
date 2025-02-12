import time, os, numpy as np
from array import array

def norm_square_list(vector):
    norm = 0
    for v in vector: norm += v*v
    return norm

def norm_square_list_comprehension(vector):
    return sum(v*v for v in vector)

def norm_square_python_arrays(vector):
    norm = 0
    for v in vector: norm += v*v
    return norm

def norm_square_np_sum(vector):
    return np.sum(vector*vector)

def norm_square_np_dot(vector):
    return np.dot(vector,vector)

if __name__ == '__main__':
    os.system('clear')

    vector       = list(range(1_000_000))
    vector_array = array('i',vector)
    vector_np    = np.array(vector)

    ex_time = time.time()
    norm_square_list(vector)
    ex_time = time.time() - ex_time
    print(f"{'='*10} norm_square_list: {ex_time:.05f} {'='*10}")


    ex_time = time.time()
    norm_square_list_comprehension(vector)
    ex_time = time.time() - ex_time
    print(f"{'='*10} norm_square_list_comprehension: {ex_time:.05f} {'='*10}")

    ex_time = time.time()
    norm_square_python_arrays(vector_array)
    ex_time = time.time() - ex_time
    print(f"{'='*10} norm_square_python_arrays: {ex_time:.05f} {'='*10}")

    ex_time = time.time()
    norm_square_np_sum(vector_np)
    ex_time = time.time() - ex_time
    print(f"{'='*10} norm_square_np_sum: {ex_time:.05f} {'='*10}")

    ex_time = time.time()
    norm_square_np_dot(vector_np)
    ex_time = time.time() - ex_time
    print(f"{'='*10} norm_square_np_dot: {ex_time:.05f} {'='*10}")