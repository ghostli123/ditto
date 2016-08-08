import pyshark
import threading
import Queue
import time
from collections import defaultdict 

from threading import Thread
import time
import random

from Queue import Queue
import glob
import os

import GlobalVariable

durationList = []
class TreeComparator:
    treeFeatureArray = []
    index = 1
    def __init__(self):
        treeFeatureArray = []
        pass
    
    @staticmethod
    def combine(item, flowTuble):
        #print "combine", item, flowTuble
        #print "combine"
        temp = []
        for i in range(len(item)):
            if i == 5:
                continue
            temp.append(item[i]|flowTuble[i])
            #item[i] = item[i]|flowTuble[i]
        temp.append(str(int(item[5]) + 1))
        #print "combine end:", tuple(temp)
        #print "combine end:", item
        #return item
        return tuple(temp)


    @staticmethod
    def merge_new(treeFeature):
        #print "in the merge now"
        flowTuble = (treeFeature.dst, treeFeature.srcport, treeFeature.t2ld, treeFeature.uri, treeFeature.packetIndex, treeFeature.hitTimes)
        flag = False
        for iterator, item in enumerate(TreeComparator.treeFeatureArray):
            tempFlag = False
            for i in range(5):
                if (len(flowTuble[i]) != 0 and (flowTuble[i] & item[i])):
                    if set(['/']) == (flowTuble[i] & item[i]):
                        tempFlag = False
                    else:
                        #print "bingo", flowTuble[i], item[i]
                        tempFlag = True
            if tempFlag == True:
                TreeComparator.treeFeatureArray[iterator] = TreeComparator.combine(item, flowTuble)
                flag = True
                GlobalVariable.log("matched tree feature array:"+"\t"+str(item)+"\n")
                break
        #if flowTuble in TreeComparator.treeFeatureArray:
        if flag == True:
            GlobalVariable.log("match\n")
            #print "match" 
            #treeFeature.show()
            pass
        else:
            GlobalVariable.log("unmatch\n")
            #print "unmatched ", flowTuble
            #treeFeature.show()
            (TreeComparator.treeFeatureArray).append(flowTuble)

            #GlobalVariable.log(str(treeFeature.flow[0])+"|"+str(treeFeature.flow[1])+"|"+str(treeFeature.flow[2])+"|"+str(treeFeature.flow[3])+"|"+str(treeFeature.flow[4])+"|"+str(treeFeature.flow[5])+"|"+str(treeFeature.flow[6])+"|"+str(treeFeature.flow[7])+"|"+str(treeFeature.flow[8])+"|"+str(treeFeature.flow[9])+"|"+str(treeFeature.flow[10])+"|"+str(treeFeature.flow[11])+"\n")    
            #GlobalVariable.log("tree feature array:"+"\t"+str(TreeComparator.index)+"\t"+str(treeFeature.flow)+"\n")
        
            #print "tree feature array:", TreeComparator.index, treeFeature.flow
            TreeComparator.index += 1
        GlobalVariable.log("merge ends"+"|"+str(len(TreeComparator.treeFeatureArray))+"|"+str(TreeComparator.treeFeatureArray)+"\n")
        GlobalVariable.log("duration:"+"\t"+str(time.time() - treeFeature.ts)+"\n")
        #print "merge ends", len(TreeComparator.treeFeatureArray), TreeComparator.treeFeatureArray
        #print "duration:", time.time() - treeFeature.ts
        durationList.append(time.time() - treeFeature.ts)
        GlobalVariable.log("average duration:"+"\t"+str(sum(durationList)/len(durationList))+"\n")
        GlobalVariable.log("end Time:"+"\t"+str(time.time())+"\n")
        #print "average duration:", sum(durationList)/len(durationList)
        #print "end Time:", time.time()

    def show(self):
        pass

