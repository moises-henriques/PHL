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

def addTpAq_tbo(file,acvDict):
    file1 = open(file, 'r')
    lines = file1.readlines()

    newFile = open("new_"+file, "w")

    flag_819 = True
    flag_820 = True
    flag_997 = True
    flag_998 = True
    flag_firstRun = True
    entryMFN = None

    for line in lines:
        if line[0:4] == '!ID ':
            if not flag_firstRun:
                if flag_819:
                    newFile.write('!v819!Pré-Migração\n')
                if flag_820:
                    newFile.write('!v820!20220623\n')
                if flag_997:
                    try:
                        newFile.write('!v997!'+acvDict[entryACV]+'\n')
                    except:
                        print('Erro no ID: '+entryMFN)
                if flag_998:
                    newFile.write('!v998!'+entryMFN+'\n')
            flag_819 = True
            flag_820 = True
            flag_997 = True
            flag_998 = True
            flag_firstRun = False
            entryMFN = line[4:11]
            newFile.write(line)
        elif line[0:6] == '!v800!':
            entryACV = line[6:].replace('\n','').lower()
            newFile.write(line)
        elif line[0:6] == '!v819!':
            newFile.write('!v819!Pré-Migração\n')
            flag_819 = False
        elif line[0:6] == '!v820!':
            newFile.write('!v820!20220623\n')
            flag_820 = False
        elif line[0:6] == '!v997!':
            newFile.write(line)
            flag_997 = False
        elif line[0:6] == '!v998!':
            newFile.write(line)
            flag_998 = False
        else:
            newFile.write(line)

file = 'phl_acv.txt'

acvDict = MFN_NomeInterno(file)

file = '001_tbo.txt'

addTpAq_tbo(file,acvDict)