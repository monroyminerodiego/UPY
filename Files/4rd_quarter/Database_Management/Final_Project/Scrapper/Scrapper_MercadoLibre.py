import os, pandas as pd, multiprocessing, threading, asyncio

import time
from random import randint

class main:
    
    # ========== CONSTRUCTOR ==========
    def __init__(self,list_of_words:list[str],cpu_cores_usage:int = 'default',threads_limit:int = 'default',verbose:bool = False):
        """
        Initializes the main class with specified configurations for processing a list of words.

        ### Args:
        - `list_of_words` (list[str]): A list of words to be processed.
        - `cpu_cores_usage` (int, optional): Number of CPU cores to use. Defaults to half of the available cores if 'default' is specified.
        - `threads_limit` (int, optional): The limit of threads to use. Defaults to the number of available CPU cores if 'default' is specified.
        - `verbose` (bool, optional): If True, enables verbose output. Defaults to False.

        ### Attributes:
        - `verbose` (bool): Controls verbose output for debugging and monitoring.
        - `cpu_cores_usage` (int): Number of CPU cores to use for processing.
        - `threads_limit` (int): Maximum number of threads to use for processing.
        - `list_of_words` (list[str]): List of words to be processed.
        - `word_status_df` (pandas.DataFrame): DataFrame tracking the processing status of each word.

        ### Methods:
        - `start_subprocess`: Starts a subprocess for managing a set of threads.
        - `start`: Initiates the main processing workflow.
        """
        # Setting variables from args
        self.verbose         = verbose
        self.cpu_cores_usage = (1 if (os.cpu_count() <= 3) else os.cpu_count() / 2) if (cpu_cores_usage == 'default') else cpu_cores_usage
        self.threads_limit   = os.cpu_count() if (threads_limit == 'default') else threads_limit
        self.list_of_words   = list(list_of_words)
        
        # Informs user about the length of the list
        if self.verbose: print(f'List with {len(self.list_of_words)} words.')
        
        # Setting variables from processes
        self.word_status_df  = self.__divide_data_into_chunks()
        

    # =============== PRIVATE METHODS ===============
    def __divide_data_into_chunks(self):
        """
        Divides the list of words into chunks for processing across multiple threads and processors.

        This method calculates the division of words based on the configured CPU cores and thread limits,
        and returns a `pandas.DataFrame` with the allocation details for each word.

        ### Returns:
        * `pandas.DataFrame`: A DataFrame containing columns for word, status, processor, and thread.
        """
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

    async def __start_thread(self,thread_id:str):
        """
        Asynchronously starts a thread for processing a chunk of data.

        ### Args:
        - `thread_id` (str): The identifier for the thread.
        """
        waiting = randint(0,20)
        await asyncio.sleep(waiting)
        return

    def __run_thread(self,thread_id:str): 
        """
        A wrapper method for running the asynchronous '__start_thread' method.

        ### Args:
        - `thread_id` (str): The identifier for the thread.

        ### Returns:
        The result of the asyncio `run` function, executing `__start_thread`.
        """
        return asyncio.run(self.__start_thread(thread_id))

    # =============== PUBLIC METHODS ===============
    def start_subprocess(self,process_id:str,runtime_dict:dict):
        """
        Starts a subprocess for managing a set of threads.

        ### Args:
        - `process_id` (str): The identifier for the subprocess.
        - `runtime_dict` (dict): A dictionary to store runtime information for each process.

        This method initializes threads based on the configured thread limit, starts them, and waits for their completion.
        It also records the runtime for each process in `runtime_dict`.
        """
        start_time = time.time()
        if self.verbose: print(f"Process {process_id} started...")
        threads = []
        for i in range(self.threads_limit):
            thread = threading.Thread(target=self.__run_thread,args=(f"{process_id}-{i}",))
            thread.start()
            threads.append(thread)

        for thread in threads:thread.join()
        
        if self.verbose: print(f"... process {process_id} ended.")

        runtime_dict[process_id] = f"{time.time()-start_time:.02f}"

    def start(self):
        """
        Initiates the main processing workflow.

        This method is the entry point for starting the word processing task. It manages subprocesses and threads,
        and oversees the overall execution and resource allocation.
        """
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

        if self.verbose: print(f"Performance timing: {runtime_dict}")



if __name__ == '__main__':
    '''
    TO-DO's:
    * Hacer validaciones creación de bases de datos
    '''
    from faker import Faker
    
    os.system('cls')
    
    fake = Faker()

    power_pct = 100

    test = main(
        list_of_words   = [fake.word() for _ in range(randint(10000,100000))],
        cpu_cores_usage = int((power_pct*os.cpu_count())/100),
        threads_limit   = int(power_pct/10),
        verbose         = True,
    )

    test.start()

    
