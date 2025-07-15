import multiprocessing
import time

class MyProcess(multiprocessing.Process):
    def __init__(self, id):
        super(MyProcess, self).__init__()
        self.id = id

    def run(self):
        time.sleep(1)
        print(f"Process with ID {self.id} executed.")
        
if __name__ == '__main__':
    processes = [MyProcess(i) for i in range(4)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
