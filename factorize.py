import multiprocessing  as mp

import os

import time


def factorize(*numbers):
    result=[]
    for num in numbers:
        factors =[]
        for i in range(1,num+1):
            if num % i == 0:
                factors.append(i)
    
        result.append(factors)
    
    return result
    
    #Синхронна версія
if __name__=="__main__":
    
    start_time = time.time()
    
    a, b, c, d  = factorize(128, 255, 99999, 10651060)
    
    end_time =time.time()

    print(f"Finish in {end_time - start_time} seconds")
    
    #Асинхронна версія
    num_cores = os.cpu_count()
    processes = []
    numbers_factorize = (128, 255, 99999, 10651060)

    for _ in range(4):
        p = mp.Process(target=factorize, args=numbers_factorize)
        p.start()
        processes.append(p)

    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"Finish in {end_time - start_time} seconds")
    
    print("Number of CPU cores:", num_cores)

    