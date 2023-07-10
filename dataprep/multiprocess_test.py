from random import random
from time import sleep
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import set_start_method
 
# task completed in a worker
def task(queue):
    # declare the queue global variable
    # generate some work
    data = random() * 5
    # block to simulate work
    sleep(data)
    # put it on the queue
    print('stuck here')
    queue.put(data)
 
# protect the entry point
if __name__ == '__main__':
    # set the fork start method
    #set_start_method('fork')
    # declare the global variable
    #global queue
    # define the queue global variable
    queue = Queue()
    # create the pool of workers
    with Pool(1) as pool:
        # issue tasks
        results = [pool.apply_async(task, queue) for _ in range(10)]
        # wait for all the tasks to complete
        for result in results:
            result.wait()
        print('here')
    # consume all items
    for i in range(1):
        # get item from queue
        print('getting')
        item = queue.qsize()
        print('got')
        # report item
        print(f'> got {item}')