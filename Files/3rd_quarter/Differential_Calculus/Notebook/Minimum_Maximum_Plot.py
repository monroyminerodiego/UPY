import os; os.system('cls')
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return (x**3) + (6 * x**2) + (9 * x) + 1

# First derivative
def f_prime(x):
    return (3 * x**2) + (12 * x) + 9

# Second derivative
def f_double_prime(x):
    return (6 * x) + 12

# Find critical points
critical_points = []
for x in np.arange(-5, 1, 0.25):
    if f_prime(x) == 0:
        critical_points.append(x)

# Classify critical points
for x in critical_points:
    if f_double_prime(x) > 0:
        print(f"Minimum point: ({x}, {f(x)})")
    elif f_double_prime(x) < 0:
        print(f"Maximum point: ({x}, {f(x)})")
    else:
        print(f"Inflection point: ({x}, {f(x)})")


# Plot the function and critical points
x = np.arange(-5, 1, 0.25)
y = f(x)
plt.plot(x, y)

for x in critical_points:
    plt.plot(x,f(x), marker='o', color='r')
    plt.annotate('(%s, %s)' % (x, f(x)), (x, f(x)), color='black')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('f(x) = x^3 + 6x^2 + 9x + 1')
plt.grid(True)
plt.show()

