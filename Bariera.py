# -*- coding: utf-8 -*-
__author__ = 'Konrad'

import threading
import time


class myThread(threading.Thread):
    threadCounter = 0
    barrierCounter = 0
    exitCounter = 0
    lock = threading.Lock()
    cv = threading.Condition(lock)

    def __enter__(self):
        return self

    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        with myThread.lock:
            myThread.threadCounter += 1

    def run(self):
        print(self.name + " is starting.")
        time.sleep(self.threadID * 2)
        print(self.name + " is ending.")
        self.barrier()
        print(self.name + " - ended")

    @staticmethod
    def barrier():
        myThread.cv.acquire()
        myThread.barrierCounter += 1
        while myThread.barrierCounter < myThread.threadCounter:
            myThread.cv.wait()
        myThread.exitCounter += 1
        if myThread.exitCounter >= myThread.threadCounter:
            myThread.exitCounter = 0
            myThread.barrierCounter = 0
        myThread.cv.notify_all()
        myThread.cv.release()

    def __exit__(self, exc_type, exc_val, exc_tb):
        with myThread.lock:
            myThread.threadCounter -= 1


with myThread(1, "Thread 1") as t1, myThread(2, "Thread 2") as t2, myThread(3, "Thread 3") as t3:
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


with myThread(1, "Thread 4") as t1, myThread(2, "Thread 5") as t2, myThread(3, "Thread 6") as t3:
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()