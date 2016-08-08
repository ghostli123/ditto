import threading
import GlobalVariable
import TreeFeature
import TreeComparator
class StabilizedTree:
    def __init__(self, growingTree):
        #print "growing tree starts"
        self.flow = growingTree.flow
        self.flowArray = growingTree.flowArray
        self.ts = growingTree.ts
        self.treeFeature = TreeFeature.TreeFeature(self)
        #print len(growingTree.flowArray)
        #if len(growingTree.flowArray) <= 1 and growingTree.flowArray[0][7] != "/":
        #if growingTree.flowArray[0][7] != "/":
        if False:
            pass
        else:
            with GlobalVariable.lock_merge:
                TreeComparator.TreeComparator.merge_new(self.treeFeature)
        pass    
        
        
        def show(self):
            pass


