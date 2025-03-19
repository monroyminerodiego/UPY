import multiprocessing

def cube(n):
    return n ** 3

if __name__ == '__main__':
    with multiprocessing.Pool(processes=4) as pool:
        results = [pool.apply_async(cube, args=(i,)) for i in range(5)]
        results = [r.get() for r in results]

    print("Results:", results)
