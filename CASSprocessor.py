import math, os, numpy, pylab, sys, datetime, random as rng

#Data Structure
    #"tupleInputs" = list of Tuples (each tuple represents a reaction)
        #0-"kVal"=float K-value of reaction
        #1-"rxns"=dictionary of ("Molecule Name":difference in coefficients)
        #2-"coeffs"=dictionary of ("Molecule Name":coefficient of REACTANTS)
    #"molCounts" = dictionary of ("Molecule Name":Provided intial number of each molecule)

def updateAll(tupleInputs, molCounts, maxTime, maxIterations, outputFreq, molVSList, inputName): #List of Tuples, dictionary of molecule counts
    append=str(datetime.datetime.now()).replace(" ","_").replace(".","").replace(":","")
    os.mkdir(r"%s_%s"%("Results",append))
    rng.seed(124213)
    time       = 0.0
    iteration  = 0

    #Prints parameters
    print "Maximum Time: ",maxTime
    print "Maximum number of Iterations: ", maxIterations
    print "Output Frequency: ", outputFreq
    print "Input File Name: ", inputName
    print "Molecules: ",
    for key in molCounts.keys():
        print key,
    print "\nPlots: ",
    for vs in molVSList:
        if((vs[0] not in molCounts and "time" not in vs[0].lower()) or vs[1] not in molCounts and "time" not in vs[1].lower()):
                print "\nError - Plotting a variable (%s) that does not exist"%("%s vs. %s"%(vs[0],vs[1]))
                sys.exit(0)
        print "%s vs. %s,"%(vs[0],vs[1]),
    print "\n------------------"
    print "Processing..."
    print "------------------"
    
    
    # open output files
    fileHandles = open_output_files(molCounts, append)
    write_titles_to_outputFiles(fileHandles, molCounts)

    while(time < maxTime and iteration < maxIterations):
        props = []
        for i in range(len(tupleInputs)): #len(tupleInputs) is the number of reactions
            prop = computePropensity(tupleInputs[i],molCounts)
            #print prop,
            props.append(prop)
        #print "\n"
        sump = sum(props)
        if(sump==0):
            print "All reaction propensities have reached 0."
            break
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
        rxnChoice = tupleInputs[count-1][2] #Dictionary of change in coefficients (Key=Molecule Name)
        molCounts = reactionUpdater(rxnChoice,molCounts)
        write_data_to_output(fileHandles, time, molCounts)
        if (iteration % outputFreq == 0):
            print "iteration %d   time %5.4g" % (iteration, time)   
        iteration += 1
    close_output_files(fileHandles)
    test = True
    if(molVSList!=None):
        graphResults(fileHandles,molCounts,molVSList,append)
    
    print "Simulation Complete - Check Folder for files"


#takes one tuple and returns propensity based on algorithm   
def computePropensity(tupleInput, molCounts):
    kVal=tupleInput[0]# k value
    coeffs=tupleInput[1] #Dictionary of coefficients for each molecule REACTANTS ONLY (Key=Molecule Name)
    num = len(coeffs)
    propProduct=kVal # initialized to k value
    for key in coeffs:
        while True:
            try:
                if(coeffs[key]>0):
                    propProduct *= (1.0*calcNPR(molCounts[key],coeffs[key])*(1.0/(coeffs[key]))) # multiplied by permutation of molCounts for each reactant molecule divided by the coefficient
                break
            except KeyError:
                print "ERROR - %s is not in the molecule list"%(key)
                sys.exit(1)
    return propProduct

#Takes two integers n and r, and returns nPr (i.e. P(n,r))
def calcNPR(n,r):
    product=1
    while(r>0):
        product*=n
        n-=1
        r-=1
    return product

#Takes one dictionary of a reaction and adds the difference for each molecule according to the reaction
def reactionUpdater(rxn,molCounts):
    for key in rxn:
        if(key in molCounts.keys()):
            #print molCounts[key], ", ", rxn[key]
            #assert(molCounts[key]>0), 'Molecule %s has ran out'%(key)
            molCounts[key]+=rxn[key]
        else:
            print "ERROR - %s Molecule not Found"%(key)
    return molCounts

#Creates writable files for each output file
#Creates folder called "Results+Date+Time" with Plot + .dat"
def open_output_files(molCounts, append):
    files = []
    for key in molCounts.keys():
        path = str(os.getcwd()) + "\\Results_" + append
        name =("%s.dat"%(key))
        os.path.join(path,name)
        files.append(open(os.path.join(path,name),"w"))#Add folder for results
    return files

def write_titles_to_outputFiles(fileHandles, molCounts):
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("Time\t  Molecule Count\n")
        i+=1

#writes data for all files
def write_data_to_output(fileHandles, time, molCounts):
    #This function writes a (time, data) pair to the corresponding output file. concentrations not molecule counts.
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("%5.4e %8.7f\n" %(time, molCounts[key]))
        #print "%5.4e %8.7f" %(time, molCounts[key])
        i+=1

#closes fileHandles to avoid problems
def close_output_files(fileHandles):
    for i in range(0,len(fileHandles)):
        fileHandles[i].close()

def graphResults(fileHandles, molCounts, molVSList, append):
    fileNames = []
    if(molVSList!=None):
        count=0
        for i in range(len(molVSList)):
            xN=molVSList[i][0]
            yN=molVSList[i][1]
            j=0
            while("time" in molVSList[i][j]):
                j+=1
            listTime=readInTime("%s.dat"%molVSList[i][j], append)
            if("time" in xN.lower()):
                listx=listTime
            else:
                listx=readIn("%s.dat"%xN,append) 
            if("time" in yN.lower()):
                listy=listTime
            else:
                listy=readIn("%s.dat"% yN,append)
            title1="%s vs. %s"%(xN,yN)
            pylab.title(title1)
            if(yN.lower()=="time"):
                pylab.plot(listy,listx)
                pylab.xlabel("Time")
                pylab.ylabel("%s Population"%(xN))
            else:
                pylab.plot(listx,listy)
                pylab.xlabel("%s Population"%(xN))
                pylab.ylabel("%s Population"%(yN))
            #x=numpy.arange(0,
            fig = pylab.gcf()
            fig.canvas.set_window_title('Computational Adaptable Stochastic Simulator')
            path = str(os.getcwd()) + "\\Results_" + append
            name =("%s_Plot_%s.png"%(title1,append))
            fig.savefig(os.path.join(path,name),dpi=100)
            pylab.show()
            pylab.close()
            
def readInTime(fileName, append):
    list1=[]
    path = str(os.getcwd()) + "\\Results_" + append
    fileDir=os.path.join(path,fileName)
    file = open(fileDir,"r")
    for line in file.readlines():
        if "Time" not in line:
            list1.append(line.split(" ",1)[0])   
    return list1
                
#Reads the created files for plotting
def readIn(fileName, append):
    list1=[]
    path = str(os.getcwd()) + "\\Results_" + append
    fileDir=os.path.join(path,fileName)
    file = open(fileDir,"r")
    for line in file.readlines():
        if "Time" not in line:
            list1.append(line.split(" ",1)[1])   
    return list1

