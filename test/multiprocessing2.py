from multiprocessing import Lock, Process, Queue, current_process, Pool, Manager
import time
import queue

# def print_func(continent="Asia"):
#     print("the name of continent is: ", continent)
#
# if __name__ == "__main__":
#     names = ["America", "Europe", "Africa", "Japan"]
#     procs = []
#     proc = Process(target=print_func)
#     procs.append(proc)
#     proc.start()
#
#     for name in names:
#         proc = Process(target=print_func, args=(name,))
#         procs.append(proc)
#         proc.start()
#
#     for proc in procs:
#         proc.join()

# colors = ["red", "blue", "green", "black"]
# cnt = 1
# queue = Queue()
# print("Pushing item to queue:")
# for color in colors:
#     print("item no: ", cnt, " ", color)
#     queue.put(color)
#     cnt += 1
#
# print("\npopping items from queue:")
# cnt = 0
# while not queue.empty():
#     print("item no: ", cnt, " ", queue.get())
#     cnt += 1

# def do_job(tasks_to_accomplish, tasks_that_are_done):
#     while True:
#         try:
#             task = tasks_to_accomplish.get_nowait()
#         except:
#             break
#         else:
#             print(task)
#             tasks_that_are_done.put(task + ' is done by ' + current_process().name)
#
#     return True
#
# def main():
#     number_of_task = 10
#     number_of_proccesses =  10
#     tasks_to_accomplish = Queue()
#     tasks_that_are_done = Queue()
#     proccesses = []
#
#     for i in range(number_of_task):
#         tasks_to_accomplish.put("Task no " + str(i))
#
#     for w in range(number_of_proccesses):
#         p = Process(target=do_job, args=(tasks_to_accomplish, tasks_that_are_done))
#         proccesses.append(p)
#         p.start()
#
#     for p in proccesses:
#         p.join()
#
#     while not tasks_that_are_done.empty():
#         print(tasks_that_are_done.get())
#
#     return True
#
# if __name__ == "__main__":
#     main()

# work = (["A",5], ["B", 2], ["C", 1], ["D", 3])
# def work_log(work_data):
#     print("Proccess %s waiting %s seconds" %(work_data[0], work_data[1]))
#     time.sleep(int(work_data[1]))
#     print("Process %s Finished."%work_data[0])
#
# def pool_handler():
#     p = Pool(5)
#     p.map(work_log, work)
#
# if __name__ == "__main__":
#     pool_handler()

def worker(procnum, return_dict):
    print(str(procnum) + "represent!")
    return_dict[procnum] = procnum

if __name__ == "__main__":
    manager = Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(5):
        p = Process(target=worker, args=(i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    print(return_dict.values())


# manager = Manager()
# return_dict = manager.dict()
# jobs = []
# # queue = Queue()
# i = 1
# for i in range(1000):
#     url = 'https://www.keys2drive.com.au/suburbs/select2_list?page=' + str(i)
#     p = Process(target=get_all_ids, args=(i, url, return_dict))
#     jobs.append(p)
#     p.start()
#
# for proc in jobs:
#     proc.join()
#
# print(return_dict)