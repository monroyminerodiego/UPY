from random import random

def pi_montecarlo(n=1000):
    in_circle = 0
    for i in range(n):
        x, y = random(), random()
        if x ** 2 + y ** 2 <= 1.0:
            in_circle += 1
    
    return 4.0 * in_circle / n