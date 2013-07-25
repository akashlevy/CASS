import CASSparser, CASSuserInputConverter, CASSprocessor, CASSoutput
import sys

def mainCASS():
    print "****************************"
    print "******Welcome to CASS!******"
    print "****************************"
    print "-This stochastic simulator is useful for modeling biochemical networks."
    print "-Make sure your file is in the correct format (See Documentation)"
    print "and verify that the file is in the current working directory\n"

    loop = True
    while(loop):
        try:
            print "Please enter your text file name (do not include .txt): ",
            fileName = str(raw_input())
            fooFile = open(fileName+".txt")
            loop=False
        except IOError:
            print "Error - File does not exist"

    #sets inputs to temporary variables for organization
    elements = CASSuserInputConverter.inputReactions(fileName)
    rxnsAndMolCounts=elements[0]
    duration=elements[1]
    maxIterations=elements[2]
    outputFreq=elements[3]
    molVSList=elements[4]
    inputName=elements[5]

    EqnsNmolCounts = CASSparser.parseText(rxnsAndMolCounts)
    tupleInputs = EqnsNmolCounts[0]
    molCounts = EqnsNmolCounts[1]

    #Calls processor
    CASSprocessor.updateAll(tupleInputs, molCounts, duration, maxIterations, outputFreq, molVSList, inputName)

mainCASS()
    
