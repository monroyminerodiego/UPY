from random import random

cpdef double pi_montecarlo(int n = 1000):
    cdef int in_circle = 0, i
    cdef double x, y

    for i in range(n):
        x, y = random(), random()
        if x ** 2 + y ** 2 <= 1.0:
            in_circle += 1

    return 4.0 * in_circle / n