import pyshark
import threading
import time
import GlobalVariable

class SniffThread(threading.Thread):
    def __init__(self, targetInputMethod, targetInputValue):
        threading.Thread.__init__(self)
        self.targetInputMethod = targetInputMethod
        self.targetInputValue = targetInputValue


    def __target_files(self, targetInputValue):
        #folder = "/home/yang/development/ditto/live/crawl/Dridex-set1"
        folder = targetInputValue
        filelist = []
        GlobalVariable.allFiles(folder, filelist)
        return filelist

    def __process_http(self, pkt):
        #print "packet is comming"
        #print pkt
        try:
            #print pkt.http
            #print dir(pkt.http)
            if pkt.http.chat.startswith("GET") or pkt.http.chat.startswith("POST"):
                #print pkt
                #print pkt.http
                if "ocsp" in pkt.http.request_full_uri or "symc" in pkt.http.request_full_uri:
                    return
                #("request", pkt.sniff_timestamp,
                #pkt.ip.src,pkt.ip.dst,pkt.tcp.srcport,pkt.tcp.dstport,
                #pkt.http.host, pkt.http.request_uri, pkt.http.request_full_uri,
                #pkt.http.accept, referer) 
                fieldExtracted = ['request', 'sniff_timestamp', 'ip.src', 'ip.dst', \
                        'tcp.srcport', 'tcp.dstport', 'http.host', \
                        'http.request_uri', 'http.request_full_uri', \
                        'http.accept', 'referer', 'packetIndex']
                for i in range(len(fieldExtracted)):
                    if '.' in fieldExtracted[i]:
                        levelOne = fieldExtracted[i][:fieldExtracted[i].find('.')]
                        levelTwo = fieldExtracted[i][fieldExtracted[i].find('.')+1:]
                        if getattr(pkt, levelOne, "") == "":
                            fieldExtracted[i] = ""
                        else:
                            fieldExtracted[i] = getattr(getattr(pkt, levelOne), levelTwo, "")
                    else:
                        fieldExtracted[i] = getattr(pkt, fieldExtracted[i], "")
                fieldExtracted[0] = 'request'
                fieldExtracted[11] = str(GlobalVariable.packetIndex)
                GlobalVariable.flowNumber += 1
                GlobalVariable.httpRequestQueue.put(fieldExtracted)
                if GlobalVariable.maxNumberHttpRequestInQueue < GlobalVariable.httpRequestQueue.qsize():
                    GlobalVariable.maxNumberHttpRequestInQueue = GlobalVariable.httpRequestQueue.qsize()
                    #print "maxNumberHttpRequestInQueue:", GlobalVariable.maxNumberHttpRequestInQueue
        except:
            pass

    def __process_dns(self, pkt):
        print "I am DNS"
        #print pkt.dns.flags_response
        #print dir(pkt.dns)
        try:
            if pkt.dns.flags_response == "0":
                print "request"
                #print pkt.dns.qry_name
                pass #this is a dns query
            else:
                print "response"
                print pkt.dns.qry_name
                print pkt.dns.resp_name
                print pkt.ip.src, pkt.ip.dst, pkt.tcp.srcport, pkt.tcp.dstport, pkt.dns.qry_name, pkt.dns.resp_name
                fieldExtracted = ['dns response', 'sniff_timestamp', 'ip.src', 'ip.dst', \
                        'tcp.srcport', 'tcp.dstport', 'dns.qry_name', 'dns.resp_name', 'packet_index']
                for i in range(len(fieldExtracted)):
                    if '.' in fieldExtracted[i]:
                        levelOne = fieldExtracted[i][:fieldExtracted[i].find('.')]
                        levelTwo = fieldExtracted[i][fieldExtracted[i].find('.')+1:]
                        if getattr(pkt, levelOne, "") == "":
                            fieldExtracted[i] = ""
                        else:
                            fieldExtracted[i] = getattr(getattr(pkt, levelOne), levelTwo, "")
                    else:
                        fieldExtracted[i] = getattr(pkt, fieldExtracted[i], "")
                fieldExtracted[0] = 'dnsresponse'
                fieldExtracted[8] = str(GlobalVariable.packetIndex)
                GlobalVariable.flowNumber += 1
                GlobalVariable.dnsResponseQueue.put(fieldExtracted)
                pass #this is a dns response
        except:
            pass

    def __process_smtp(self, pkt):
        print "I am smtp"
        print dir(pkt.smtp)
        print pkt.smtp

    def __process_ftp(self, pkt):
        print "I am ftp"
        print dir(pkt.ftp)
        print pkt.ftp

    def __process_packet(self, pkt):
        pass
        GlobalVariable.packetIndex += 1
        highest_layer = pkt.highest_layer
        #print "highest layer:", highest_layer
        #process = {'HTTP':self.__process_http, 'DNS':self.__process_dns, 'SMTP':self.__process_smtp, 'FTP':self.__process_ftp}
        process = {'HTTP':self.__process_http}
        #process = {'DNS':self.__process_dns}
        #process = {'SMTP':self.__process_smtp}
        try:
            process.get(highest_layer)(pkt)
            pass
        except:
            pass

    def __sniff_offline(self, filename):
        #capture = pyshark.FileCapture(filename, keep_packets=False, display_filter='http')
        capture = pyshark.FileCapture(filename, keep_packets=False)
        capture.apply_on_packets(self.__process_packet)
        #capture.apply_on_packets(self.__process_dns)
        if GlobalVariable.flowNumber > 0:
                GlobalVariable.validPcapNumber += 1
        GlobalVariable.totalPcapNumber += 1
        print "flowNumber:", GlobalVariable.flowNumber, "validPcapNumber:", GlobalVariable.validPcapNumber, "totalPcapNumber:", GlobalVariable.totalPcapNumber

    def __sniff_online(self, targetInterface):
        #capture = pyshark.FileCapture(filename, keep_packets=False, display_filter='http')
        capture = pyshark.LiveCapture(interface=targetInterface)
        capture.apply_on_packets(self.__process_packet)
        #capture.apply_on_packets(self.__process_dns)
        if GlobalVariable.flowNumber > 0:
                GlobalVariable.validPcapNumber += 1
        GlobalVariable.totalPcapNumber += 1
        print "flowNumber:", GlobalVariable.flowNumber, "validPcapNumber:", GlobalVariable.validPcapNumber, "totalPcapNumber:", GlobalVariable.totalPcapNumber

    def run(self):
        GlobalVariable.log("sniff start Time:"+"\t"+str(time.time())+"\n")
        if self.targetInputMethod == "-i":
            self.__sniff_online(self.targetInputValue)
            pass
        elif self.targetInputMethod == "-p":
            self.__sniff_offline(self.targetInputValue)
            pass
        elif self.targetInputMethod == "-d":
            filelist = self.__target_files(self.targetInputValue)
            for filename in filelist:
                print filename
                self.__sniff_offline(filename)
        print "going to finish sniff"
        GlobalVariable.finishSniffing = True
        GlobalVariable.httpRequestQueue.put("END OF THE SYSTEM")
        GlobalVariable.dnsResponseQueue.put("END OF THE SYSTEM")
        GlobalVariable.smtpQueue.put("END OF THE SYSTEM")
        GlobalVariable.ftpQueue.put("END OF THE SYSTEM")
        #print "sniff finish label has been set"
