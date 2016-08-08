import threading
import time

import GlobalVariable
import GrowingTree

class ConsumeDNSResponseQueueThread(threading.Thread):
    def __init__(self):
        super(ConsumeDNSResponseQueueThread, self).__init__()
        self.growingTreeArray = []
        self.growingTreeIndex = 0
        self.lock = threading.Lock()
    
    def growingTreeCallBack(self, index):
        print "to delete growing tree index;", index, len(self.growingTreeArray)
        with self.lock:
            self.growingTreeArray[:] = [tup for tup in self.growingTreeArray if tup.index == index]

    def run(self):
        GlobalVariable.log("consume start Time:"+"\t"+str(time.time())+"\n")
        #time.sleep(1)
        while(not GlobalVariable.finishSniffing or not GlobalVariable.dnsResponseQueue.empty()):
            if (not GlobalVariable.dnsResponseQueue.empty()):
                print "CONSUMER EMPTY dns"
                continue
            dnsResponse = GlobalVariable.dnsResponseQueue.get()
            if dnsResponse == "END OF THE SYSTEM":
                break

            flowValue = dnsResponse

            if len(self.growingTreeArray) > 0:
                print "growingTree is larger than 0"
                flag = False
                print "DEBUG 1"
                for growingTree in self.growingTreeArray:
                    #if not growingTree.isActivatedtivated():
                        #continue
                    ifAppended = growingTree.tryAddingNode(flowValue)
                    if ifAppended == True:
                        flag = True
                        break
                    else:
                        pass
                print "DEBUG 2", flag
                if flag == False:
                    if flowValue[10] != "":
                        continue
                    self.growingTreeIndex += 1
                    GlobalVariable.log("flag == False"+"\t"+str(self.growingTreeIndex)+"\t"+str(flowValue)+"\n")
                    print "flag == False", self.growingTreeIndex, flowValue 
                    ts = time.time()
                    growingTree = GrowingTree.GrowingTree(self.growingTreeIndex,flowValue, ts, parent = self)
                    with self.lock:
                        self.growingTreeArray.append(growingTree)
            else:
                print "growingTree is equal to 0"
                if flowValue[10] != "":
                    continue
                self.growingTreeIndex += 1
                GlobalVariable.log("no trees"+"\t"+str(self.growingTreeIndex)+"\t"+str(flowValue))
                print "no trees", self.growingTreeIndex, flowValue
                ts = time.time()
                growingTree = GrowingTree.GrowingTree(self.growingTreeIndex,flowValue, ts, parent = self)
                with self.lock:
                    self.growingTreeArray.append(growingTree)
            print "loop loop loop", GlobalVariable.finishSniffing, GlobalVariable.dnsResponseQueue.empty()

        print "not stucked any more"
        GlobalVariable.log(str(len(self.growingTreeArray))+"\t"+str(self.growingTreeIndex))
        print len(self.growingTreeArray), self.growingTreeIndex
        print "the end of consume"

