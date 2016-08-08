import threading
import Queue
import time
from collections import defaultdict 

import GlobalVariable
from threading import Thread
import WatchDogThread
from Queue import Queue
import StabilizedTree

class GrowingTree(threading.Thread):
    def __init__(self, index, flow, ts, parent = None):
        super(GrowingTree, self).__init__()
        #print "in the growing tree now"
        self.ts = ts
        self.sinal = threading.Event()
        self.queue = Queue(1)
        self.watchDogThread = WatchDogThread.WatchDogThread(self.sinal, self.queue, parent = self)
        self.watchDogThread.start()
        #WatchDogThread.WatchDogThread(self.sinal,self.queue, parent = self).start()
        #print "in the growing tree init"
        self.flow = flow
        self.index = index
        self.flowArray = []
        self.flowArray.append(self.flow)
        self.parent = parent
        #print "last step of growing tree init"
        #print flow
        pass

    def watchDogCallBack(self):
        #print "call back from watch dog"
        self.parent.growingTreeCallBack(self.index)
        stabilizedTree = StabilizedTree.StabilizedTree(self)

    def show(self):
        pass

    def __process_smtp(self, pkt):
        pass

    def __process_ftp(self, pkt):
        pass

    def __process_dns(self, pkt):
        pass


    def __compare_http_http(self, flow, item):
        if (item[4] != "" and flow[4] == item[4]) or (item[8] != "" and flow[10] == item[8]) or (item[7] != "" and item[7] != "/" and flow[7] == item[7]) or (item[6] != "" and flow[6] == item[6]) or (item[3] != "" and flow[3] == item[3]) or (item[6] != "" and GlobalVariable.hostnameTop2LevelDomain(flow[6]) == GlobalVariable.hostnameTop2LevelDomain(item[6])):
            if abs(float(flow[1]) - float(item[1])) > 10:
                #flagLargerThanFive = False
                #print "going to return false"
                return False
            self.flowArray.append(flow)
            #if "apple" in ",".join(flow) and "microsoft" in ",".join(item):
            #if "apple" in flow[6]:
                #print "growing tree append:", flow, item
            if self.queue.empty():
                self.queue.put(1)
            return True
        else:
            return False

    def __compare_http_dns(self, flow, item):
        if (item[3] != "" and flow[3] == item[3]) or (item[4] != "" and flow[4] == item[4]) or (item[6] != "" and flow[6] == item[6]) or (item[3] != "" and flow[7] == item[3]):
            self.flowArray.append(flow)
            print flow[1], item[1]
            if abs(float(flow[1]) - float(item[1])) > 10:
                #flagLargerThanFive = False
                #print "going to return false"
                return False

            if self.queue.empty():
                self.queue.put(1)
            return True
        else:
            return False

    def __compare_http_smtp(self, flow, item):
        pass

    def __compare_http_ftp(self, flow, item):
        pass

    def __process_http(self, flow, flowArray):
        process = {'request':self.__compare_http_http, 'dnsresponse':self.__compare_http_dns, 'SMTP':self.__compare_http_smtp, 'FTP':self.__compare_http_ftp}
        for item in flowArray:
            return process.get(item[0])(flow, item)
            #return __compare_http_http(flow, item)
            #if http, xxx
            #if dns, xxx
            pass

        pass

    def tryAddingNode(self, flow):
        process = {'request':self.__process_http, 'dnsresponse':self.__process_dns, 'SMTP':self.__process_smtp, 'FTP':self.__process_ftp}
        return process.get(flow[0])(flow, self.flowArray)

    def __join__(self):
        #print "self.watchDogThread.join()"
        self.watchDogThread.join()
        #print "self.watchDogThread.join() done"

    
        '''
        if flow[0] == "request":
            for item in self.flowArray:
                if (item[4] != "" and flow[4] == item[4]) or (item[8] != "" and flow[10] == item[8]) or (item[7] != "" and flow[7] == item[7]) or (item[6] != "" and flow[6] == item[6]) or (item[3] != "" and flow[3] == item[3]) or (item[6] != "" and GlobalVariable.hostnameTop2LevelDomain(flow[6]) == GlobalVariable.hostnameTop2LevelDomain(item[6])):
                    self.flowArray.append(flow)
                    print flow[1], item[1]
                    if abs(float(flow[1]) - float(item[1])) > 10:
                        #flagLargerThanFive = False
                        print "going to return false"
                        return False

                    if self.queue.empty():
                        self.queue.put(1)
                    return True
                else:
                    return False
        if flow[0] == "dnsResponse":
            for item in self.flowArray:
                if (item[4] != ""):
                    pass
        '''
    
        '''
        if flow in self.flowArray:
            if self.queue.empty():
        	self.queue.put(1)
            #print "catched", flow, self.queue.qsize(), self.queue.empty()
            #self.queue.put(1)
            #print "after catched", flow, self.queue.qsize(), self.queue.empty()
            return True
        else:
            #print "not catched", flow
            return False
        '''
    def appendResponse(self, httpResponse):
        pass
 
 
