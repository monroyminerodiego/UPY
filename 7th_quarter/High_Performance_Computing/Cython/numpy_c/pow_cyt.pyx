import numpy as np
cimport numpy as cnp

# Ensure NumPy is initialized properly
cnp.import_array()

# Define an explicit NumPy integer type
ctypedef cnp.int32_t INT_DTYPE

def powers_array_cy(int N):
    # Correct the data type definition
    cdef cnp.ndarray[INT_DTYPE, ndim=2] data
    
    # Ensure NumPy array is explicitly int32
    data = np.arange(N * N, dtype=np.int32).reshape((N, N))

    for i in range(N):
        for j in range(N):
            data[i, j] = i ** j

    return data  # Returning full matrix, not just row 2
