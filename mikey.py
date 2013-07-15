import math, numpy, pylab, sys, random as rng

#Data Structure
    #"tupleInputs" = list of Tuples (each tuple represents a reaction)
        #0-"kVal"=float K-value of reaction
        #1-"rxns"=dictionary of ("Molecule Name":difference in coefficients)
        #2-"coeffs"=dictionary of ("Molecule Name":coefficient of REACTANTS)
    #"molCounts" = dictionary of ("Molecule Name":Provided intial number of each molecule)

def updateAll(tupleInputs, molCounts): #List of Tuples, dictionary of molecule counts
    rng.seed(124213)
    time       = 0.0
    iteration  = 0                               #Iteration count (TO DO - make this a parameter)
    outputFreq = 1000                            #Output frequency (TO DO - make this a parameter)
    updaters   = []
    maxTime = 10
    maxIterations = 1000000

    #Open output files
    fileHandles = open_output_files(molCounts)
    loop=True
    while(time < maxTime and iteration < maxIterations and loop):
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
        rxnChoice = tupleInputs[count-1][1] #Dictionary of change in coefficients (Key = Molecule Name)
        molCounts = reactionUpdater(rxnChoice,molCounts)
        if (iteration % outputFreq == 0):
            tempTime= time
            write_data_to_output(fileHandles, time, molCounts)
            print "iteration %d   time %5.4g" % (iteration, time)   
        iteration += 1
        loop = (isNotZero(molCounts))
    close_output_files(fileHandles)
    graphResults(fileHandles,molCounts)
    
    print "Simulation Complete - Check Folder for files"

#Checks to see if any of the molecules have reached a zero count (TODO - We need to decide what happens when this occurs)
def isNotZero(molCounts):
    bool1=True
    for num in molCounts:
        if(num==0):
            bool1=False
    return bool1

#Takes one tuple and returns propensity based on algorithm   
def computePropensity(tupleInput, molCounts):
    kVal = tupleInput[0]#K-value
    coeffs = tupleInput[2] #Dictionary of coefficients for each molecule REACTANTS ONLY (Key = Molecule Name)
    num = len(coeffs)
    propProduct = kVal #Initialized to k-value
    for key in coeffs:
        try:
            propProduct *= calcNPR(molCounts[key],coeffs[key])*(1.0/(coeffs[key])) #Multiplied by permutation of molCounts for each reactant molecule divided by the coefficient
            break
        except KeyError:
            raise ParsingSyntaxError("ERROR: %s is not in the molecule list" %(key))
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

def perm(n):
    x=1
    product=x
    while(x<=n):
        product=product*x
        x+=1
    return product

#Takes one dictionary of a reaction and adds the difference for each molecule according to the reaction
def reactionUpdater(rxn,molCounts):
    for key in rxn:
        if(key in molCounts.keys()):
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

#Graphs all combinations and creates output files --> C(n,2) total plots)
def graphResults(fileHandles,molCounts):
    fileNames = []
    directoryName="C:\Users\Admin\Documents\MIKEY\Mike's School Docs\Extracurricular\Summer 2013 - PGSS\PGSS-CS\Biochemical Stochastic Simulator\Tests"
    for key in molCounts.keys():
        fileNames.append("%s.dat"%key)
    for i in range(len(fileNames)):
        for j in range(i+1,len(fileNames)):
            if(fileNames[i] !=fileNames[j]):
                listx=readIn(fileNames[i])
                listy=readIn(fileNames[j])
                xN=fileNames[i].replace(".dat","")
                yN=fileNames[j].replace(".dat","")
                pylab.plot(listx,listy)
                title1="%s vs. %s"%(xN,yN)
                pylab.title(title1)
                pylab.xlabel("%s Population"%(xN))
                pylab.ylabel("%s Population"%(yN))
                fig = pylab.gcf()
                fig.canvas.set_window_title('Adaptable Stochastic Simulator')
                #fig.savefig(("%s%s.plot"%(directoryName,title1)),dpi=100) #TO DO - Does not save properly
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
    updateAll(tupleInputsEx, molCountsEx)
    
main()
