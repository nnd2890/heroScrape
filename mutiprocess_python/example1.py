from multiprocessing import Pool
import time

def f(n):
    sum = 0
    for x in range(1000):
         sum += x * x
    return sum

if __name__=="__main__":
    t1 = time.time()
    p = Pool()
    result1 = p.map(f, range(10000))
    # print(result1)
    p.close()
    p.join()
    print("Pool took: ", time.time() - t1)

    t2 = time.time()
    result2 = []
    for x in range(100000):
        result2.append(f(x))
    print("Pool took: ", time.time() - t2)