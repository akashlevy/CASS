import math, os, numpy, pylab, datetime, time as tm, random as rng
import CASSoutput

#Input Data Structure
    #"tupleInputs" = list of Tuples (each tuple represents a reaction)
        #0-"kVal"=float K-value of reaction
        #1-"rxns"=dictionary of ("Molecule Name":difference in coefficients)
        #2-"coeffs"=dictionary of ("Molecule Name":coefficient of reactants)
    #"molCounts" = dictionary of ("Molecule Name": Provided intial number of each molecule)
    #"maxTime" = input parameter representing the maximum time the program can run
    #"maxIterations" = input parameter representing the maximum number of iterations the program should run
    #"outputFreq" = the frequency of outputs for every number of iterations
    #"molVSList" = a list of tuples of strings representing the molecules/time to be plotted against each other
    #"inputName" = a string representing the name of the input file

def updateAll(tupleInputs, molCounts, maxTime, maxIterations, outputFreq, molVSList, seed=1234213, silent=False):
    #Initialize variables
    rng.seed(seed)
    time = 0.0
    iteration = 0

    #Prints parameters if not silent
    if not silent:
        print "Maximum Time: ", maxTime
        print "Maximum number of Iterations: ", maxIterations
        print "Output Frequency: ", outputFreq
        print "Molecules: ",
        for key in molCounts.keys():
            print key,
        print "\nPlots: ",
        if molVSList != None:
            for vs in molVSList:
                if((vs[0] not in molCounts and "time" not in vs[0].lower()) or (vs[1] not in molCounts and "time" not in vs[1].lower())):
                        raise ProcessingError("\nError - Plotting variables (%s) that do not exist"%("%s vs. %s"%(vs[0],vs[1])))
                print "%s vs. %s,"%(vs[0],vs[1]),

        #Processing message
        print "\n------------------"
        print "Processing..."
        print "------------------"
    
    #Creates new directory and opens output files
    suffix=str(datetime.datetime.now()).replace(" ","_").replace(".","").replace(":","")
    os.mkdir(r"Results_%s"%(suffix))
    fileHandles = open_output_files(molCounts, suffix)
    write_titles_to_outputFiles(fileHandles, molCounts)

    #The Gillespie Algorithm will continue to run until 1 of 3 events occurs:
        #1. The simulated time reaches the user-input maximum time
        #2. The number of iterations reaches the user-input maximum number of iterations
        #3. All reaction propensities reach 0 (i.e. all reactions ran to completion or insufficient reactants remain for any new products)

    #Start timer
    start_time = tm.time()

    #Gillespie Algorithm
    while(time < maxTime and iteration < maxIterations):
        props = [] #list of propensity values for each reaction
        
        for i in range(len(tupleInputs)): #len(tupleInputs) is the number of reactions
            prop = computePropensity(tupleInputs[i],molCounts)
            props.append(prop)
            
        sump = sum(props)
        if (sump==0):
            if not silent:
                print "All reaction propensities have reached 0. The system has reached equilibrium"
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
        rxnChoice = tupleInputs[count-1][2] #dictionary of change in coefficients (Key=Molecule Name)
        molCounts = reactionUpdater(rxnChoice,molCounts)
        write_data_to_output(fileHandles, time, molCounts)
        if (iteration % outputFreq == 0):
            if not silent:
                print "iteration %d   time %5.4g" % (iteration, time)   
        iteration += 1

    #Close output file handles
    close_output_files(fileHandles)

    #Stop timer
    end_time = tm.time()

    #Display time elapsed
    if(molVSList != None):
    #    print "Time Elapsed = " + str(end_time - start_time)
        return (fileHandles, molCounts, molVSList, suffix)

#Takes one tuple and returns propensity based on Gillespie Algorithm   
def computePropensity(tupleInput, molCounts):
    kVal=tupleInput[0] #k-value
    coeffs=tupleInput[1] #dictionary of coefficients for each molecule reactants only(key=Molecule Name)
    propProduct=kVal #multiplicative-accumulator is initialized to the reaction k-value
    for key in coeffs:
        while True:
            try:
                if (coeffs[key] > 0):
                    #Multiplied by permutation of molCounts for each reactant molecule divided by the coefficient
                    #(e.g. The propensity of reactants 3A + 2B is: (1/3*(N_A)*(N_A-1)*(N_A-2))*(1/2*(N_B)*(N_B-1)))
                    propProduct *= (1.0*calcNPR(molCounts[key],coeffs[key])*(1.0/(coeffs[key])))
                break
            except KeyError:
                raise ProcessingError("ERROR - %s is not in the molecule list"%(key))
    return propProduct

#Takes two integers n and r, and returns the permutation: nPr (i.e. P(n,r))
#Returns 0 if r > n
def calcNPR(n,r):
    product=1
    while(r>0):
        product*=n
        n-=1
        r-=1
    return product

#Takes one dictionary of a reaction and adds the difference for each molecule according to the reaction
def reactionUpdater(rxn,molCounts):
    #Updates all molecule counts based on chosen reaction
    for key in rxn:
        if(key in molCounts.keys()):
            molCounts[key]+=rxn[key] #corresponds molecules based on key name
        else:
            raise ProcessingError("ERROR - %s Molecule not Found"%(key))
    return molCounts

#Creates writable files for each output file
#Creates folder called "Results+Date+Time" with Plots and Molecule.dat txt files
def open_output_files(molCounts, suffix):
    files = []
    for key in molCounts.keys():
        path = str(os.getcwd()) + "\\Results_" + suffix
        name =("%s.dat"%(key))
        os.path.join(path,name)
        #Add folder for results
        files.append(open(os.path.join(path,name),"w"))
    return files

#Writes title headers on each output file "Time" and "Molecule Count"
def write_titles_to_outputFiles(fileHandles, molCounts):
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("Time\t  Molecule Count\n")
        i+=1

#Writes data for all files
def write_data_to_output(fileHandles, time, molCounts):
    #This function writes a (time, data) pair to the corresponding output file. concentrations not molecule counts.
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("%5.4e %8.7f\n" %(time, molCounts[key]))
        i+=1

#Closes fileHandles to avoid errors
def close_output_files(fileHandles):
    for i in range(0,len(fileHandles)):
        fileHandles[i].close()
