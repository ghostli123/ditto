import threading
import time

import GlobalVariable
import GrowingTree

class ConsumeRequestQueueThread(threading.Thread):
    def __init__(self):
        super(ConsumeRequestQueueThread, self).__init__()
        self.growingTreeArray = []
        self.growingTreeIndex = 0
        self.lock = threading.Lock()
        
    def growingTreeCallBack(self, index):
        #print "to delete growing tree index;", index, len(self.growingTreeArray)
        #self.growingTreeArray[index].__join__()

        with self.lock:
            self.growingTreeArray[:] = [tup for tup in self.growingTreeArray if tup.index != index]

    def run(self):
        GlobalVariable.log("consume start Time:"+"\t"+str(time.time())+"\n")
        #time.sleep(1)
        while(not GlobalVariable.finishSniffing or not GlobalVariable.httpRequestQueue.empty()):
            #print "coming AAAAAAAAAAA"
            if (GlobalVariable.httpRequestQueue.empty()):
                #print "CONSUMER EMPTY http"
                continue
            httpRequest = GlobalVariable.httpRequestQueue.get()
            if httpRequest == "END OF THE SYSTEM":
                break

            flowValue = httpRequest

            if len(self.growingTreeArray) > 0:
                #print "growingTree is larger than 0"
                flag = False
                #print "DEBUG 1"
                for growingTree in self.growingTreeArray:
                    #if not growingTree.isActivatedtivated():
                        #continue
                    ifAppended = growingTree.tryAddingNode(flowValue)
                    if ifAppended == True:
                        flag = True
                        break
                    else:
                        pass
                #print "DEBUG 2", flag
                if flag == False:
                    if flowValue[10] != "":
                        continue
                    GlobalVariable.log("flag == False"+"\t"+str(self.growingTreeIndex)+"\t"+str(flowValue)+"\n")
                    print "flag == False", self.growingTreeIndex, flowValue 
                    ts = time.time()
                    growingTree = GrowingTree.GrowingTree(self.growingTreeIndex,flowValue, ts, parent = self)
                    with self.lock:
                        self.growingTreeArray.append(growingTree)
                    self.growingTreeIndex += 1
            else:
                #print "growingTree is equal to 0"
                if flowValue[10] != "":
                    continue
                GlobalVariable.log("no trees"+"\t"+str(self.growingTreeIndex)+"\t"+str(flowValue))
                #print "no trees", self.growingTreeIndex, flowValue
                ts = time.time()
                growingTree = GrowingTree.GrowingTree(self.growingTreeIndex,flowValue, ts, parent = self)
                with self.lock:
                    self.growingTreeArray.append(growingTree)
                self.growingTreeIndex += 1
            #print "loop loop loop", GlobalVariable.finishSniffing, GlobalVariable.httpRequestQueue.empty()

        pass # add join here
        for growingTree in self.growingTreeArray:
            #print "number of growing Tree:", len(self.growingTreeArray)
            growingTree.__join__()
            
        time.sleep(5)
        print "not stucked any more"
        GlobalVariable.log(str(len(self.growingTreeArray))+"\t"+str(self.growingTreeIndex))
        #print len(self.growingTreeArray)
        print "the end of consume"



