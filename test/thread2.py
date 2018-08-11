import threading
import _thread
import time

# def worker(num):
#     print("worker: %s" %num)
#     return
#
# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker, args=(i,))
#     threads.append(t)
#     t.start()

# def worker():
#     print(threading.current_thread().getName(), "Starting")
#     time.sleep(2)
#     print(threading.current_thread().getName(), "Exsiting")
#
# def my_service():
#     print(threading.current_thread().getName(), "Starting")
#     time.sleep(3)
#     print(threading.current_thread().getName(), "Exsiting")
#
# t = threading.Thread(name='my_service', target=my_service)
# w = threading.Thread(name='worker', target=worker)
# w2 = threading.Thread(target=worker)
#
# w.start()
# w2.start()
# t.start()

# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print("%s: %s" %(threadName, time.ctime(time.time())))
#
# try:
#     _thread.start_new_thread(print_time, ("Thread-1", 2,))
#     _thread.start_new_thread(print_time, ("Thread-2", 5,))
# except:
#     print("Error: Unable to start thread")
#
# while 1:
#     pass

ex

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        threading.Lock().acquire()
        print_time(self.name, self.counter, 3)
        threading.Lock().release()

def print_time(threadName, delay, counter):
    while counter:
        time.sleep(delay)
        print("%s: %s" %(threadName, time.ctime(time.time())))
        counter -= 1

theadLock = threading.Lock()
threads = []

thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Exiting Main Thread")