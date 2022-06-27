import os
path = os.getcwd()+'/PHL/'
os.chdir(path)

def extractTp(file,**kwargs):
    if 'flagList' in kwargs:
        flagList = kwargs.get('flagList')
    else:
        flagList = False
    if flagList:
        file1 = open(file, 'r')
        lines = file1.readlines()
        newFile = open("List_"+file, "w")

        tpList = []
        for line in lines:
            if line[0:6] == '!v300!':
                entryID = line[6:].replace('\n','').lower()
                tpList.append(entryID)
                newFile.write(entryID+'\n')

        return tpList
    else:
        file1 = open(file, 'r')
        lines = file1.readlines()

        tpDict = {}
        for line in lines:
            if line[0:4] == '!ID ':
                entryMFN = int(line[4:11])
            if line[0:6] == '!v300!':
                entryID = line[6:].replace('\n','')
                tpDict[entryMFN] = entryID

        return tpDict

def correctACV(file,cntDict,idmDict):
    file1 = open(file, 'r')
    lines = file1.readlines()

    newFile = open("new_"+file, "w")

    for line in lines:
        if line[0:6] == '!v040!':
            try:
                idm = idmDict[int(line[6:])]
                newLine = '!v040!'+idm+'\n'
                newFile.write(newLine)
            except:
                newFile.write(line)
        elif line[0:6] == '!v071!':
            cnt = cntDict[int(line[6:])]
            newLine = '!v071!'+cnt+'\n'
            newFile.write(newLine)
        else:
            newFile.write(line)

file = 'phl_cnt.txt'

cntDict = extractTp(file)

file = 'phl_idm.txt'

idmDict = extractTp(file)

file = 'phl_acv.txt'

correctACV(file,cntDict,idmDict)