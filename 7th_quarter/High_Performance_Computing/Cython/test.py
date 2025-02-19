from pi_estimator_c.pi_estimator_cython import pi_montecarlo #type: ignore
from pi_estimator_c.pi_estimator import pi_montecarlo as pi_m_python
from numpy_c.pow_cyt import powers_array_cy #type: ignore
import time, os

if __name__ == '__main__':
    os.system('clear')

    ex_time = time.time()
    result = pi_montecarlo(1_000_000)
    ex_time = time.time() - ex_time
    print(f"{'='*10} Cython {'='*10}\n{result}\n{'='*10} Ex Time: {ex_time:0.8f} {'='*10}")

    ex_time = time.time()
    result = pi_m_python(1_000_000)
    ex_time = time.time() - ex_time
    print(f"{'='*10} Python {'='*10}\n{result}\n{'='*10} Ex Time: {ex_time:0.6f} {'='*10}")

    ex_time = time.time()
    result = powers_array_cy(3)
    ex_time = time.time() - ex_time
    print(f"{'='*10} Numpy C {'='*10}\n{result}\n{'='*10} Ex Time: {ex_time:0.6f} {'='*10}")