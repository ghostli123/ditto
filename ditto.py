import threading
import sys
from SniffThread import SniffThread
from ConsumeRequestQueueThread import ConsumeRequestQueueThread

def main():
    try:
        if len(sys.argv) < 3:
            print 'No action specified'
            sys.exit()
        thread1 = SniffThread(sys.argv[1], sys.argv[2])
        thread2 = ConsumeRequestQueueThread()
        thread1.start()
        thread2.start()
    except Exception as e:
        print str(e)
    finally:
        if thread1.isAlive():
            thread1.join()
        if thread2.isAlive():
            thread2.join()
        print "system finish"


if __name__=="__main__":
    main()
