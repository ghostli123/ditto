import GlobalVariable
class TreeFeature:
    def __init__(self, stabilizedTree):
        self.hitTimes = 1
        self.flow = stabilizedTree.flow
        self.ts = stabilizedTree.ts
        self.flowArray = stabilizedTree.flowArray
        self.dst = []
        self.srcport = []
        #self.host = []
        self.t2ld = []
        self.uri = []
        self.packetIndex = []
        
        for item in self.flowArray:
            if item[0] == "request":
                dst = item[3]
                srcport = item[4]
                t2ld = GlobalVariable.hostnameTop2LevelDomain(item[6])
                uri = item[7]
                packetIndex = item[11]
                if dst != "":
                    self.dst.append(dst)
                if srcport != "":
                    self.srcport.append(srcport)
                if t2ld != "":
                    self.t2ld.append(t2ld)
                if uri != "":
                    self.uri.append(uri)
                self.packetIndex.append(packetIndex)
            if item[0] == "dnsresponse":
                self.packetIndex.append(item[8])
            
        self.dst = set(self.dst)
        self.srcport = set(self.srcport)
        self.t2ld = set(self.t2ld)
        self.uri = set(self.uri)
        self.packetIndex = set(self.packetIndex)


        def show(self):
            return self.flow


