import os, requests, pandas as pd, multiprocessing, threading, asyncio
from bs4 import BeautifulSoup
from wintoast import ToastNotifier

import time
from random import randint

class Scrapper_MercadoLibre:
    
    # ========== CONSTRUCTOR ==========
    def __init__(self,list_of_words:list[str],cpu_cores_usage:int = 'default',threads_limit:int = 'default',verbose:bool = False):
        '''
        '''
        # Setting variables
        self.list_of_words   = list(list_of_words)
        self.verbose         = verbose
        self.cpu_cores_usage = (1 if (os.cpu_count() <= 3) else os.cpu_count() / 2) if (cpu_cores_usage == 'default') else cpu_cores_usage
        self.threads_limit   = os.cpu_count() if (threads_limit == 'default') else threads_limit
        self.word_status_df  = self.__divide_data_into_chunks()
        # self.manager = multiprocessing.Manager()
        

    # =============== MAIN METHODS ===============
    def __divide_data_into_chunks(self):
        '''
        '''
        # Informing user about the usage of the resources
        if self.verbose: print(f'Dividing data into {self.cpu_cores_usage} processes and {self.threads_limit} threads, making {int((int(len(self.list_of_words)/self.cpu_cores_usage)+1)/self.threads_limit)} words per thread...')

        # The data is divided into processors and threads
        processor_count, thread_count = 1, 1
        processors_list, thread_list  = [], []
        for _ in range(1,len(self.list_of_words)+1):
            processors_list.append(processor_count)
            thread_list.append(thread_count)
            thread_count     = 1 if self.threads_limit   < thread_count    + 1  else (thread_count + 1 if processor_count + 1 > self.cpu_cores_usage else thread_count)
            processor_count  = 1 if self.cpu_cores_usage < processor_count + 1  else processor_count  + 1

        # Data returned as a 'pandas.DataFrame' object
        return pd.DataFrame(data = {
            'Word' : self.list_of_words,
            'Status' : 'Queue',
            'Processor' : processors_list,
            'Thread' : thread_list
        })


    # =============== THREAD METHODS ===============
    async def __start_thread(self,thread_id:str):
        '''
        '''
        waiting = randint(0,20)
        await asyncio.sleep(waiting)
        return


    # =============== ACTIVATORS ===============
    def __run_thread(self,thread_id:str): return asyncio.run(self.__start_thread(thread_id))

    def start_subprocess(self,process_id:str,runtime_dict:dict):
        '''
        '''
        start_time = time.time()
        if self.verbose: print(f"Process {process_id} started...")
        threads = []
        for i in range(self.threads_limit):
            thread = threading.Thread(target=self.__run_thread,args=(f"{process_id}-{i}",))
            thread.start()
            threads.append(thread)

        for thread in threads:thread.join()
        
        if self.verbose: print(f"... {process_id} ended.")

        runtime_dict[process_id] = f"{time.time()-start_time:.02f}"

    
    def start(self):
        '''
        '''
        # Informs user about the length of the list
        if self.verbose: print(f'List with {len(self.list_of_words)} words.')

        manager      = multiprocessing.Manager()
        runtime_dict = manager.dict()

        # Starts the process for every sub_process
        processes = []
        for i in range(1,self.cpu_cores_usage+1):
            process = multiprocessing.Process(target=self.start_subprocess,args=(i,runtime_dict))
            process.start()
            processes.append(process)

        # Once every process finished their execution, it joins the processes
        for process in processes:
            process.join()

        print(runtime_dict)



if __name__ == '__main__':
    '''


    TO-DO's:
    * Hacer validaciones creación de bases de datos


    '''
    from faker import Faker
    
    os.system('cls')
    
    fake = Faker()

    power_pct = 30

    test = Scrapper_MercadoLibre(
        list_of_words   = [fake.word() for _ in range(randint(500,1000))],
        cpu_cores_usage = int((power_pct*os.cpu_count())/100),
        threads_limit   = int(power_pct/10),
        verbose         = True,
    )

    test.start()

    
