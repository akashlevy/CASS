import parse
import userInputToStringLists
import CASSprocesser

def mainCASS():
    print "****************************"
    print "******Welcome to CASS!******"
    print "****************************"
    print "-This stochastic simulator is"
    print "useful for modeling"
    print "biochemical networks."

    print "Make sure your file is in the correct format (See Documentation)\n and make sure it is in the current working directory\n"

    loop = True
    while(loop):
        try:
            print "Please enter your text file name (do not include .txt): ",
            fileName = str(raw_input())
            loop=False
        except IOError:
            print "Error - File does not exist"
        
    elements = userInputToStringLists.inputReactions(fileName)
    #print elements
    rxnsAndMolCounts=elements[0]
    duration=elements[1]
    maxIterations=elements[2]
    outputFreq=elements[3]
    molVSList=elements[4]
    inputName=elements[5]

    EqnsNmolCounts = parse.parseText(rxnsAndMolCounts)
    #print EqnsNmolCounts
    tupleInputs = EqnsNmolCounts[0]
    molCounts = EqnsNmolCounts[1]

    StochSimCompute_Becich_v5.updateAll(tupleInputs, molCounts, duration, maxIterations, outputFreq, molVSList, inputName)

mainCASS()
