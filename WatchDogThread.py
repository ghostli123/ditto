import threading
import time
import GrowingTree
import GlobalVariable

class WatchDogThread(threading.Thread):
    def __init__(self, event, queue, parent = None):
        super(WatchDogThread, self).__init__()
        self.threadEvent = event
        self.queue = queue
        self.parent = parent

    def run(self):
        #print "watchdog thread is running"
        remainingTime = 5
        while remainingTime > 0:
            #print "watchdog thread is in the loop"
            if True:
                if self.queue.empty():
                   pass
                else:
                    #print "watchDog queueSize Before ", self.queue.qsize()
                    num = self.queue.get()
                    #print "watchDog queueSize After ", self.queue.qsize()
                    remainingTime = 5
                    #self.queue.task_done()
                    #print "Consumed", num
            #print "remainingTime: ", remainingTime
            remainingTime -= 1
            time.sleep(1)
        GlobalVariable.log("watchDog set threadEvent\n")
        #print "watchDog thread is going to finish"
        #self.threadEvent.set()
        self.parent.watchDogCallBack()
        #print "watchDog thread finishes"
