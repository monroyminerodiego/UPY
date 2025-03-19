import multiprocessing

class SafeCounterProcess(multiprocessing.Process):
    def __init__(self, counter, lock):
        super().__init__()
        self.counter = counter
        self.lock = lock

    def run(self):
        for _ in range(1000):
            with self.lock:  # Lock ensures exclusive access
                self.counter.value += 1

def main():
    counter = multiprocessing.Value('i', 0)  # Shared integer variable
    lock = multiprocessing.Lock()  # Lock to prevent race conditions
    processes = [SafeCounterProcess(counter, lock) for _ in range(4)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print("Final Counter Value (Expected: 4000):", counter.value)

if __name__ == "__main__":
    main()
