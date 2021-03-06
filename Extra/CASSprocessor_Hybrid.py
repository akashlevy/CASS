import math, os, numpy, pylab, sys, datetime, time, random as rng
import CASSoutput

#TO-DO: Catch for negative Populations! TRICKY TRICKY -Ask Markus

#Data Structure
    #"tupleInputs" = list of Tuples (each tuple represents a reaction)
        #0-"kVal"=float K-value of reaction
        #1-"coeffs"=dictionary of ("Molecule Name":coefficient of reactants)
        #2-"rxns"=dictionary of ("Molecule Name":difference in coefficients)
        
    #"molCounts" = dictionary of ("Molecule Name": Provided intial number of each molecule)
    #"maxTime" = input parameter representing the maximum time the program can run
    #"maxIterations" = input parameter representing the maximum number of iterations the program should run
    #"outputFreq" = the frequency of outputs for every number of iterations
    #"molVSList" = a list of tuples of strings representing the molecules/time to be plotted against each other
    #"inputName" = a string representing the name of the input file

class ProcessingError(Exception):
    def __init__(self, string):
        #Print error message
        print string
        print
        print "The program will now exit."
        sys.exit(1)

def updateAll(tupleInputs, molCounts, maxTime, maxIterations, outputFreq, molVSList, inputName= None, n_critical=2):
    rng.seed(124213)#SEED RANDOMLY BASED ON INPUT
    timer       = 0.0
    iteration  = 0
    t1counter=0
    t2counter=0
    tcounter=0

    #Prints parameters
    print "Maximum Time: ", maxTime
    print "Maximum Number of Iterations: ", maxIterations
    print "Output Frequency: ", outputFreq
    print "Input File Name: ", inputName
    print "Molecules: ",
    for key in molCounts.keys():
        print key,
    print "\nPlots: ",
    if molVSList !=None:
        for vs in molVSList:
            if((vs[0] not in molCounts and "time" not in vs[0].lower()) or (vs[1] not in molCounts and "time" not in vs[1].lower())):
                    raise ProcessingError("\nError - Plotting variables (%s) that do not exist"%("%s vs. %s"%(vs[0],vs[1])))
            print "%s vs. %s,"%(vs[0],vs[1]),
    print "\n------------------"
    print "Processing..."
    print "------------------"
    
    #Creates new directory and opens output files
    suffix=str(datetime.datetime.now()).replace(" ","_").replace(".","").replace(":","")
    os.mkdir(r"%s_%s"%("Results",suffix))
    fileHandles = open_output_files(molCounts, suffix)
    write_titles_to_outputFiles(fileHandles, molCounts)

    #The Gillespie Algorithm will continue to run until 1 of 3 events occurs:
        #1. The simulated time reaches the user-input maximum time
        #2. The number of iterations reaches the user-input maximum number of iterations
        #3. All reaction propensities reach 0 (i.e. all reactions ran to completion or insufficient reactants remain for any new products)
    #Hybrid gillespie algorithm
    
    start_time = time.time()#Initializes real time counter
    while(timer < maxTime and iteration < maxIterations):
        props = [] #list of propensity values for each reaction
        nonCritRxns = {}
        propRxn = {}
        for i in range(len(tupleInputs)):#Goes through all reactions tupleInputs[i][0-2]
            prop = computePropensity(tupleInputs[i],molCounts)
            props.append(prop)
            propRxn[i]=prop
            maxFires=calcMaxFires(tupleInputs[i],molCounts)
            #print maxFires, calcMaxFires(tupleInputs[i],molCounts)
            #Lower n_critical means the program will stop tau-leaping earlier
            #print str(i) + ". " + str(maxFires)
            if(maxFires > n_critical and prop > 0):
                #print "here " + str(maxFires)
                nonCritRxns[i]=tupleInputs[i]
            #propRxn[tupleInputs[i]]=prop
            
        sump=sum(props)
        if(sump==0):
            print "All reaction propensities have reached 0. The system has reached equilibrium"
            break
        rand_1 = rng.random()
        tau = (1.0/sump * math.log(1.0/rand_1))
        timer += tau
        rand_2    = rng.random()
        threshold = sump * rand_2
        summation = 0
        count     = 0
        while(threshold > summation):
            summation += props[count]
            count += 1
            tcounter +=1
        rxnChoice = tupleInputs[count-1][2] #Dictionary of change in coefficients (Key=Molecule Name)
        reactionUpdater(rxnChoice,molCounts)

        ###############Tau-Leaping###################
        #print nonCritRxns
        #print molCounts
        #print propRxn
        if(len(nonCritRxns)==0):
            tau_prime=sys.maxint
        else:
            numFires=0
            alpha=0
            counter=0
            sumC = 0.0
            for ncr in nonCritRxns.keys(): #ncr is the key to the dictionary (an integer)
                sumC+=propRxn[ncr]
                for molecule in molCounts:
                    if molecule in nonCritRxns[ncr][2]:
                        #print "entered"
                        alpha+=1.0*(propRxn[ncr]/sump)*nonCritRxns[ncr][2][molecule] #*molCounts[molecule]
            epsilon =0.03
            mu = 0
            
            for ncr in nonCritRxns.keys():#ncr is again a key
                mu+=(alpha*propRxn[ncr])
            sigma=0
            for ncr in nonCritRxns.keys():#ncr is again a key
                sigma+=((alpha**2)*propRxn[ncr])     
            #print alpha,mu,sigma
            tau_prime = min(epsilon*props[count-1]/abs(mu),(epsilon*props[count-1])**2/mu**2)
            #print alpha, tau_prime
            #print propRxn, molCounts
        
        if(tau_prime < (10*1.0/props[count-1])):
            #print "Tau Prime was less than 10/propensity"
            tau_prime2 = numpy.random.exponential(1.0/sumC)
            #print "tau' = " + str(tau_prime) + " tau'' = " + str(tau_prime2)
            if(tau_prime < tau_prime2):
                #print "Tau' was less than Tau''"
                for index in range(len(tupleInputs)):
                    z=0
                    if(index in nonCritRxns.keys()):#not critical
                        #print "numFires"
                        numFires=numpy.random.poisson(tau_prime*propRxn[index])
                    else:#critical
                        numFires=0
                    while(z < numFires):
                        reactionUpdater(tupleInputs[index][2], molCounts)
                        z+=1
                        iteration+=1
                        timer+=tau_prime/numFires
                        t1counter+=1
            else:
##                val = int(rng.random()*(len(tupleInputs)-len(nonCritRxns)))
                for index in range(len(tupleInputs)):
                    z=0
                    if index in nonCritRxns.keys(): #not critical
                        numFires=numpy.random.poisson(tau_prime2*propRxn[index])
##                    elif(index == val):
##                        numFires=0
##                        val=-1
                    else:#critical
                        numFires=0
                    
                    while(z < numFires):
                        reactionUpdater(tupleInputs[index][2], molCounts)
                        z+=1
                        iteration+=1
                        timer+=tau_prime2/numFires
                        t2counter+=1
            #write_data_to_output(fileHandles, time, molCounts)
        write_data_to_output(fileHandles, timer, molCounts)
        if (iteration % outputFreq == 0):
            print "iteration %d   time %5.4g" % (iteration, timer)   
        iteration += 1
    end_time = time.time()
    close_output_files(fileHandles)
    if(molVSList!=None):
        print "Tau Counter: " + str(tcounter)
        print "Tau' Counter: " + str(t1counter)
        print "Tau'' Counter: " + str(t2counter)
        print "Time Elapsed = " + str(end_time - start_time)
        return CASSoutput.graphResults(fileHandles,molCounts,molVSList,suffix)
    
#Assumes change is negative
#returns the maximum # of fires a rxn can occur without expiring a molecule (LR)
def calcMaxFires(tupleInput,molCounts):
    changes=tupleInput[2]
    minMF=sys.maxint
    for key in changes.keys():
        if(changes[key]<0):
            if(abs(1.0*molCounts[key]/changes[key]) < minMF):
                minMF=abs(molCounts[key]/changes[key])
    return int(minMF)
        

#takes one tuple and returns propensity based on Gillespie Algorithm   
def computePropensity(tupleInput, molCounts):
    kVal=tupleInput[0]# k-value
    coeffs=tupleInput[1] #Dictionary of coefficients for each molecule reactants only(key=Molecule Name)
    propProduct=kVal # the multiplicative-accumulator is initialized to the reaction k-value
    for key in coeffs:
        while True:
            try:
                if(coeffs[key]>0):
                    # multiplied by permutation of molCounts for each reactant molecule divided by the coefficient
                    #(e.g. The propensity of reactants 3A + 2B is: (1/3*(N_A)*(N_A-1)*(N_A-2))*(1/2*(N_B)*(N_B-1)))
                    propProduct *= (1.0*calcNPR(molCounts[key],coeffs[key])*(1.0/(coeffs[key])))
                break
            except KeyError:
                raise ProcessingError("ERROR - %s is not in the molecule list"%(key))
    return propProduct

#Takes two integers n and r, and returns nPr (i.e. P(n,r))
#Permutation function which returns 0 if r>n
def calcNPR(n,r):
    product=1
    while(r>0):
        product*=n
        n-=1
        r-=1
    return product

#Takes one dictionary of a reaction and adds the difference for each molecule according to the reaction
#returns False if the next update will cause out of bounds
def reactionUpdater(rxn,molCounts):
    #Updates all molecule counts based on chosen reaction
    for key in rxn:
        if(key in molCounts.keys()):
            molCounts[key] += rxn[key] #corresponds molecules based on key name
            #assert(molCounts[key]>0), 'Molecule %s has ran out'%(key)
        else:
            raise ProcessingError("ERROR - %s Molecule not Found"%(key))
##    if any((molCounts[key] + rxn[key])< 0 for key in rxn):
##        print "Molecule " + key + " ran out"
##        return False
##    else:
##        return True

#checks to see if molecules have ran to zero
def isNotZero(molCounts):
    bool1=True
    for num in molCounts:
        if(num==0):
            print "Warning - A molecule has reached 0"
            bool1=False
    return bool1

#Creates writable files for each output file
#Creates folder called "Results+Date+Time" with Plots and Molecule.dat txt files
def open_output_files(molCounts, suffix):
    files = []
    for key in molCounts.keys():
        path = str(os.getcwd()) + "\\Results_" + suffix
        name =("%s.dat"%(key))
        os.path.join(path,name)
        files.append(open(os.path.join(path,name),"w"))#Add folder for results
    return files

#Writes title headers on each output file "Time" and "Molecule Count"
def write_titles_to_outputFiles(fileHandles, molCounts):
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("Time\t  Molecule Count\n")
        i+=1

#writes data for all files
def write_data_to_output(fileHandles, timer, molCounts):
    #This function writes a (time, data) pair to the corresponding output file. concentrations not molecule counts.
    i=0
    for key in molCounts.keys():
        fileHandles[i].write("%5.4e %8.7f\n" %(timer, molCounts[key]))
        i+=1

#closes fileHandles to avoid problems
def close_output_files(fileHandles):
    for i in range(0,len(fileHandles)):
        fileHandles[i].close()
