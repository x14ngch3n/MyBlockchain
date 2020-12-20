# from itertools import count
# from hashlib import sha256

# msg = 'test pow'

# for i in count():
#     hashid = sha256((msg + str(i)).encode()).hexdigest()
#     print(i, hashid)
#     if hashid.startswith('000'):
#         print('success!')
#         break

# from threading import Thread
# import time

# def test():
#     print(time.time())
#     time.sleep(2)
#     print('test')

# def main():
#     thread_array = {}
#     for i in range(10):
#         t = Thread(target=test)
#         t.start()
#         thread_array[i] = t

#     for i in range(10):
#         thread_array[i].join()

# if __name__ == "__main__":
#     main()

# from threading import Thread
# import time
# from time import ctime, sleep

# def my_counter():

#     print('test1')
#     sleep(1)
#     print('test2')
#     return True

# def main():
#     thread_array = {}
#     start_time = time.time()
#     for tid in range(2):
#         t = Thread(target=my_counter)
#         t.start()
#         thread_array[tid] = t
#         print("%s is running thread_array[%d]" % (ctime(), tid))
#     for i in range(2):
#         thread_array[i].join()
#         print("%s thread_array[%d] ended" % (ctime(), i))
#     end_time = time.time()
#     print("Total time:{}".format(end_time - start_time))

# if __name__ == '__main__':
#     main()

# from multiprocessing import Process
# import os, time
# import psutil

# def run_proc(name):
#     for i in range(20):
#         print('我是子进程，我正在运行中')
#         time.sleep(1)

# if __name__ == '__main__':
#     #创建并启动子进程
#     p = Process(target=run_proc, args=('test', ))
#     p.start()
#     pid = p.pid  #获取子进程的pid

#     #测试暂停子进程
#     time.sleep(9)
#     pause = psutil.Process(pid)  #传入子进程的pid
#     pause.suspend()  #暂停子进程
#     print('子进程暂停运行')
#     time.sleep(9)
#     pause.resume()  #恢复子进程
#     print('\n子进程已恢复运行')
# from threading import Semaphore

# def main():
#     """
#     docstring
#     """
#     sem = Semaphore(0)
#     sem.acquire()

# if __name__ == '__main__':
#     main()
# import threading
# import time
# import inspect
# import ctypes

# def _async_raise(tid, exctype):
#     """raises the exception, performs cleanup if needed"""
#     tid = ctypes.c_long(tid)
#     if not inspect.isclass(exctype):
#         exctype = type(exctype)
#     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
#                                                      ctypes.py_object(exctype))
#     if res == 0:
#         raise ValueError("invalid thread id")
#     elif res != 1:
#         # """if it returns a number greater than one, you're in trouble,
#         # and you should call it again with exc=NULL to revert the effect"""
#         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
#         raise SystemError("PyThreadState_SetAsyncExc failed")

# def stop_thread(thread):
#     _async_raise(thread.ident, SystemExit)

# def test():
#     while True:
#         print('-------')
#         time.sleep(0.5)

# if __name__ == "__main__":
#     t = threading.Thread(target=test)
#     t.start()
#     time.sleep(5.2)
#     print("main thread sleep finish")
#     stop_thread(t)
# import threading

# def prt_hello():
#     while 1:
#         print('hello')

# if __name__ == '__main__':
#     t = threading.Thread(target=prt_hello)
#     t.setDaemon(True)
#     t.start()
from threading import Semaphore


def f(a):
    print(a)


a = Semaphore(1)
print(a)
f(a)
