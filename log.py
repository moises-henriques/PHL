import os
path = os.getcwd()+'/PHL/'
os.chdir(path)

def MFN_NomeInterno(file):
    file1 = open(file, 'r')
    lines = file1.readlines()

    acvDict = {}
    for line in lines:
        if line[0:4] == '!ID ':
            entryMFN = line[4:11]
        if line[0:6] == '!v002!':
            entryID = line[6:].replace('\n','').lower()
            acvDict[entryID] = entryMFN

    return acvDict

def MFN_NomeUsuario(file):
    file1 = open(file, 'r')
    lines = file1.readlines()

    usrDict = {}
    for line in lines:
        if line[0:4] == '!ID ':
            entryMFN = line[4:11]
        if line[0:6] == '!v701!':
            entryID = line[6:].replace('\n','').lower()
            usrDict[entryID] = entryMFN

    return usrDict

def getField(line,field,**kwargs):
    if 'remove' in kwargs:
        line = line.replace(kwargs.get('remove'),'')
    itens = line.split('^')
    for item in itens:
        if len(item) >0:
            if item[0] == field:
                return item.replace(field,'').lower()

def addMFN_log(file,usrDict,acvDict):
    file1 = open(file, 'r')
    lines = file1.readlines()

    newFile = open("new_"+file, "w")

    for line in lines:
        if line[0:4] == '!ID ':
            newFile.write(line)
            if line == '!ID 0000037\n':
                continue
        if line[0:6] == '!v910!':
            try:
                usr = usrDict[getField(line,'u')]
                newLine = line.replace('\n','')
                newLine += '^k'+usr+'\n'
            except:
                newLine = line
            
            try:
                acv = acvDict[getField(newLine,'a')]
                newLine = newLine.replace('\n','')
                newLine += '^f'+acv+'\n'
            except:
                continue
            newFile.write(newLine)

file = 'phl_acv.txt'

acvDict = MFN_NomeInterno(file)

file = 'phl_usr.txt'

usrDict = MFN_NomeUsuario(file)

file = '001_log.txt'

addMFN_log(file,usrDict,acvDict)