import random
import multiprocessing

# Serial version
def pi_serial(samples=1_000_000):
    hits = 0
    for _ in range(samples):
        x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
        if x**2 + y**2 <= 1:
            hits += 1
    return 4.0 * hits / samples

# Parallel version (apply_async)
def sample():
    x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
    return 1 if x**2 + y**2 <= 1 else 0

def pi_apply_async(samples=1_000_000):
    with multiprocessing.Pool() as pool:
        results_async = [pool.apply_async(sample) for _ in range(samples)]
        hits = sum(r.get() for r in results_async)
    return 4.0 * hits / samples

# Optimized parallel version (apply_async with chunking)
def sample_multiple(samples_partial):
    return sum(sample() for _ in range(samples_partial))

def pi_apply_async_chunked(samples=1_000_000, n_tasks=10):
    chunk_size = samples // n_tasks
    with multiprocessing.Pool() as pool:
        results_async = [pool.apply_async(sample_multiple, args=(chunk_size,)) for _ in range(n_tasks)]
        hits = sum(r.get() for r in results_async)
    return 4.0 * hits / samples

if __name__ == "__main__":
    samples = 10_000_000
    print("Pi (Serial):", pi_serial(samples))
    print("Pi (apply_async):", pi_apply_async(samples))
    print("Pi (apply_async_chunked):", pi_apply_async_chunked(samples))
