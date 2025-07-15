import multiprocessing

class CounterProcess(multiprocessing.Process):
    def __init__(self, counter):
        super().__init__()
        self.counter = counter

    def run(self):
        for _ in range(1000):
            self.counter.value += 1  # No lock, leading to race condition

def main():
    counter = multiprocessing.Value('i', 0)  # Shared integer variable
    processes = [CounterProcess(counter) for _ in range(4)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print("Final Counter Value (Expected: 4000):", counter.value)

if __name__ == "__main__":
    main()
