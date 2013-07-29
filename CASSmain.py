import CASSparser, CASSprocessor, CASSoutput

def mainCASS():
    print "****************************"
    print "******Welcome to CASS!******"
    print "****************************"
    print "-This stochastic simulator is useful for modeling biochemical networks."
    print "-Make sure your file is in the correct format (See Documentation)"
    print "-Verify that the file is in the current working directory\n"

    fileOK = False
    while not fileOK:
        try:
            print "Please enter your text file name (do not include .txt):",
            fileName = str(raw_input())
            fooFile = open(fileName + ".txt")
            fileOK = False
        except IOError:
            print "Error - File does not exist"

    #Sets inputs to temporary variables for organization
    equations, moleCounts, duration, max_iterations, output_freq, plots = CASSparser.parseText(fooFile.readlines())
    print equations
    print moleCounts

    #Calls processor
    CASSprocessor.updateAll(tupleInputs, molCounts, duration, maxIterations, outputFreq, molVSList, inputName)

mainCASS()
    
