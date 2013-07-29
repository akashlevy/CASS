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
            fileOK = True
        except IOError:
            print "Error - File does not exist"

    #Calls parser        
    equations, moleCounts, duration, max_iterations, output_freq, plots = CASSparser.parseText(fooFile.readlines())

    #Calls processor
    CASSprocessor.updateAll(equations, moleCounts, duration, max_iterations, output_freq, plots, fileName)

mainCASS()
