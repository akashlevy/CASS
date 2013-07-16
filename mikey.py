import math, os, numpy, pylab, sys, random as rng

#Data Structure
    #"tupleInputs" = list of Tuples (each tuple represents a reaction)
        #0-"kVal"=float K-value of reaction
        #1-"rxns"=dictionary of ("Molecule Name":difference in coefficients)
        #2-"coeffs"=dictionary of ("Molecule Name":coefficient of REACTANTS)
    #"molCounts" = dictionary of ("Molecule Name":Provided intial number of each molecule)

def updateAll(tupleInputs, molCounts, maxTime, maxIterations, outputFreq, molVSList, inputName): #List of Tuples, dictionary of molecule counts
##    directory=os.path.dirname(path.realpath(inputName))#Akash I need your help with directories
##    
##    =(r""+directory + "_Results_%s"%(str(datetime.datetime.now())))#ADDS DATE/TIME TO Folder Name, later stores all results in folder
##    try:
##        os.mkdir()
##    except OSError as exc: 
##        if exc.errno == errno.EEXIST and os.path.isdir(path):
##            pass
    rng.seed(124213)
    time       = 0.0
    iteration  = 0

    #Prints parameters
    print "Maximum Time: ",maxTime
    print "Maximum number of Iterations: ", maxIterations
    print "Output Frequency: ", outputFreq
    print "Input File Name: ", inputName
    print "Plots: ",
    for vs in molVSList:
        print "%s vs. %s,"%(vs[0],vs[1]),
    print "\n------------------"
    print "Processing..."
    print "------------------"
    
    
    # open output files
    fileHandles = open_output_files(molCounts)

    while(time < maxTime and iteration < maxIterations):
        props = []
        for i in range(len(tupleInputs)): #len(tupleInputs) is the number of reactions
            prop = computePropensity(tupleInputs[i],molCounts)
            props.append(prop)
        sump = sum(props)
        rand_1 = rng.random()
        tau = (1.0/sump * math.log(1.0/rand_1))
        time += tau
        rand_2    = rng.random()
        threshold = sump * rand_2
        summation = 0
        count     = 0
        while(threshold > summation):
            summation += props[count]
            count += 1
        rxnChoice = tupleInputs[count-1][1] #Dictionary of change in coefficients (Key=Molecule Name)
        molCounts = reactionUpdater(rxnChoice,molCounts)
        if (iteration % outputFreq == 0):
            tempTime= time
            write_data_to_output(fileHandles, time, molCounts)
            print "iteration %d   time %5.4g" % (iteration, time)   
        iteration += 1
    close_output_files(fileHandles)
    if(molVSList!=None):
        graphResults2(fileHandles,molCounts,molVSList,"outFile")
    
    print "Simulation Complete - Check Folder for files"


#takes one tuple and returns propensity based on algorithm   
def computePropensity(tupleInput, molCounts):
    kVal=tupleInput[0]# k value
    coeffs=tupleInput[2] #Dictionary of coefficients for each molecule REACTANTS ONLY(Key=Molecule Name)
    num = len(coeffs)
    propProduct=kVal # initialized to k value
    for key in coeffs:
        try:
            propProduct *= calcNPR(molCounts[key],coeffs[key])*(1.0/(coeffs[key])) # multiplied by permutation of molCounts for each reactant molecule divided by the coefficient
            break
        except KeyError:
            print "ERROR - %s is not in the molecule list"%(key) # REPLACE WITH RAISE ERROR
            sys.exit(1)
    return propProduct

#Takes two integers n and r, and returns nPr (i.e. P(n,r))
def calcNPR(n,r):
    product=1
    while(n>0 and r>0):
        product*=n
        n-=1
        r-=1
    return product

#Takes one dictionary of a reaction and adds the difference for each molecule according to the reaction
def reactionUpdater(rxn,molCounts):
    for key in rxn:
        if(key in molCounts.keys()):
            #print molCounts[key], ", ", rxn[key]
            molCounts[key]+=rxn[key]
        else:
            print "ERROR - %s Molecule not Found"%(key)
    return molCounts

#Creates writable files for each output file
#Creates folder called "Results+Date+Time" with Plot + .dat"
def open_output_files(molCounts):
    files = []
    for key in molCounts.keys():
        files.append(open(("%s.dat"%(key)),"w"))#Add folder for results
    return files

#writes data for all files
def write_data_to_output(fileHandles, time, molCounts):
    #This function writes a (time, data) pair to the corresponding output file. concentrations not molecule counts.
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("%5.4e %8.7f\n" %(time, molCounts[key]))
        i+=1

#closes fileHandles to avoid problems
def close_output_files(fileHandles):
    for i in range(0,len(fileHandles)):
        fileHandles[i].close()

def graphResults2(fileHandles, molCounts, molVSList, OFdirectory):
    fileNames = []
    for i in range(len(molVSList)):
        xN=molVSList[i][0]
        yN=molVSList[i][1]
        listx=readIn("%s.dat"%xN)
        listy=readIn("%s.dat"%yN)
        title1="%s vs. %s"%(xN,yN)
        pylab.plot(listx,listy)
        pylab.title(title1)
        pylab.xlabel("%s Population"%(xN))
        pylab.ylabel("%s Population"%(yN))
        fig = pylab.gcf()
        fig.canvas.set_window_title('Adaptable Stochastic Simulator')
        fig.savefig(("%s_Plot.png"%(title1)),dpi=100) ##TO DO-Add outfile directory
        pylab.show()
        pylab.close()
        
                
#Reads the created files for plotting
def readIn(fileName):
    list1=[]
    file = open(fileName,"r")
    for line in file.readlines():
        list1.append(line.split(" ",1)[1])   
    return list1

def main():
    tupleInputsEx = ((10,{"R":1},{"R":1}),
                     (.01,{"R":-1,"W":1},{"R":1,"W":1}),
                     (10,{"W":-1},{"W":1}))
    molCountsEx = {"R":1000,"W":2000}

    
    #http://en.wikipedia.org/wiki/Oregonator
    #(kVal,{Dictionary of DifferenceValues - "Molecule Name":Difference},Dictionary of DifferenceValues - "Molecule Name":Difference})
    tupleInputsEx2= (5,{"A":-1,"Y":-1,"X":1,"P":1},{"A":1,"Y":1}),(3,{"X":-1,"Y":-1,"P":2},{"X":1,"Y":1}),(10,{"A":-1,"X":1,"Z":2},{"A":1,"X":1}),(20,{"X":-2,"A":1,"P":1},{"X":2,"A":1,"P":1}),(.7,{"B":-1,"Z":-1,"Y":1},{"B":1,"Z":1}),
    molCountsEx2 = {"A":100,"B":100,"X":200,"Y":200,"Z":100,"P":100}

    updateAll(tupleInputsEx, molCountsEx, 10, 100000, 1000,(('R','W'),('W','R')), "test1")
    
main()
