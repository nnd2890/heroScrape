import os
from multiprocessing import Process, current_process, Lock, Pool, Queue

# def doubler(number):
#     result = number * 2
#     proc_name = current_process().name
#     print('{0} doubled to {1} by process id: {2}'.format(number, result, proc_name))
#
# if __name__ == "__main__":
#     numbers = [5,10,15,20,25,30, 35, 40]
#     procs = []
#     proc = Process(target=doubler, args=(5,))
#
#     for index, number in enumerate(numbers):
#         proc = Process(target=doubler, args=(number,))
#         procs.append(proc)
#         proc.start()
#
#     proc = Process(target=doubler, name="Test", args=(2,))
#     procs.append(proc)
#     proc.start()
#
#     for proc in procs:
#         proc.join()


# def printer(item, lock):
#     lock.acquire()
#     try:
#         print(item)
#     finally:
#         lock.release()
#
# if __name__ == "__main__":
#     lock = Lock()
#     items = ['tango', 'foxtrot', 10]
#     for item in items:
#         p = Process(target=printer, args=(item, lock))
#         p.start()

# def doubler(number):
#     return number * 2
#
# if __name__ == "__main__":
#     # numbers = [5,10,20]
#     pool = Pool(processes=3)
#     # print(pool.map(doubler, numbers))
#     result = pool.apply_async(doubler, (25,))
#     print(result.get(timeout=1))

sentinel = -1


def creator(data, q):
    """
    Creates data to be consumed and waits for the consumer
    to finish processing
    """
    print('Creating data and putting it on the queue')
    for item in data:
        q.put(item)


def my_consumer(q):
    """
    Consumes some data and works on it

    In this case, all it does is double the input
    """
    while True:
        data = q.get()
        print('data found to be processed: {}'.format(data))
        processed = data * 2
        print(processed)

        if data is sentinel:
            break


if __name__ == '__main__':
    q = Queue()
    data = [5, 10, 13, -1]
    process_one = Process(target=creator, args=(data, q))
    process_two = Process(target=my_consumer, args=(q,))
    process_one.start()
    process_two.start()

    q.close()
    q.join_thread()

    process_one.join()
    process_two.join()