import sys
import os.path
import os

def inputReactions(inputName):
    file = open("%s.txt"%(inputName), 'r')
    strList = file.readlines()
    index=0
    rxnsAndMolCounts = []

    #Main parser for reactions and molecule counts
    while("Reactions" not in strList[index]):
        index+=1
    while("end" not in strList[index+1]):
        index+=1
        rxnsAndMolCounts.append(strList[index])
    while("Molecule Count of Reactants" not in strList[index]):
        index+=1
    while("end" not in strList[index+1]):
        index+=1
        rxnsAndMolCounts.append(strList[index])

    #parser for optional parameters - if no integer is present, value is set to default
    #DEFAULT VALUES#
    duration = 30
    maxIterations = 1000000
    outputFreq=1000
    ################
    optionalParams=[]
    while("Optional Parameters" not in strList[index]):
        index+=1
    while("end" not in strList[index+1]):
        index+=1
        optionalParams.append(strList[index])
    for i in range(3):
        for s in optionalParams[i].split():
            if s.isdigit():
                value = int(s)     
                if(i==0):
                    duration=value
                if(i==1):
                    maxIterations=value
                if(i==2):
                    outputFreq=value
                break   
    molVSList = []
    stList = optionalParams[3].replace(',','').replace('.','').split()
    test=False
    for i in range(len(stList)):
        if(stList[i] =="vs"):
            molVSList.append((stList[i-1],stList[i+1]))
            test=True
    if(test):
        return (rxnsAndMolCounts, duration, maxIterations, outputFreq, molVSList, inputName)
    else:
        return (rxnsAndMolCounts, duration, maxIterations, outputFreq, None, inputName)

#TODO - Must check that all plot requests are in molCounts!
#print inputReactions("test1")


