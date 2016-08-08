writeToResult = open("result.txt", "w")

def fetchRecordIndex(line):
    if line == "":
        return 0
    else:
        elements = line.split("|")
        return elements[1]

def result(str):
    writeToResult.writelines(str+"\n")
    writeToResult.flush()

def parseResult():
    fileRead = open("log.txt")
    lastRecord = ""
    for line in fileRead:
        if line.startswith("merge ends"):
            currentRecord = line.strip()
            currentIndex = fetchRecordIndex(currentRecord)
            lastIndex = fetchRecordIndex(lastRecord)
            if currentIndex != lastIndex:
                pass
            else:
                pass
            lastRecord = currentRecord
    #print lastRecord
    lastRecord = lastRecord.replace("set(","")
    temp = lastRecord[lastRecord.find("[")+1:-1]
    #print temp
    temp = temp.replace("]), ", "], \n")
    temp = temp.replace("), ", ") \n\n")

    result(temp)
    writeToResult.close()
    fileRead.close()
    print "parsed result is stored in file \"result.txt\" now"
    print "output format: (grouped flow features)\\n"
    print "grouped flow features: [dst ip], [src port], [l2dn], [uri], [flowID], hit times"

if __name__=="__main__":
    parseResult()
