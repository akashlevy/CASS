import CASSparser, CASSprocessor, CASSoutput, CASSgui
import argparse, subprocess, sys

#CASS Version constant
CASSVersion = "1.0"

def main(argv=None):
    #Parse arguments
    parser = argparse.ArgumentParser()
    parser.description = "CASS: Computational Adaptable Stochastic Simulator"
    parser.epilog = "Without any arguments, the GUI will open."
    parser.prog = "cass"
    parser.conflict_handler = "resolve"
    parser.add_argument("-d", "--duration", metavar = "TIME", type = int, default = -1, help = "Manually specify a duration")
    parser.add_argument("-f", "--file", metavar = "FILE", help = "Specify a file to process")
    parser.add_argument("-fh", "--format-help", action = "store_true", help = "Display help on how to format your input files")
    parser.add_argument("-i", "--interactive", action = "store_true", help = "Interactive mode (off by default)")
    parser.add_argument("-mi", "--max-iters", metavar = "ITERS", type = int, default = -1, help = "Manually specify a maximum number of iterations")
    parser.add_argument("-of", "--output-freq", metavar = "FREQ", type = int, default = -1, help = "Manually specify a maximum number of iterations")
    parser.add_argument("-ng", "--no-graphs", action = "store_true", help = "Don't display graphs after done processing (off by default)")
    parser.add_argument("-s", "--silent", action = "store_true", help = "Don't display output while processing")
    parser.add_argument("-sd", "--seed", metavar = "NUM", help = "Specify a random seed to run the simulation with")
    parser.add_argument("-v", "--version", action = "version", version = parser.prog + "_" + CASSVersion)
    args = parser.parse_args()

    if args.format_help:
        #Help on how to manually format your files
        print
        print "Write equations in the following format (without < or >):"
        print "<Reactant1> + <Reactant2> + ... -> <Product1> + ... + <ProductN> [Reaction Rate]"
        print
        print "Write initial molecule numbers in the following format:"
        print "<Reactant1> = <Number of Molecules of Reactant1>"
        print "<Reactant2> = <Number of Molecules of Reactant2>"
        print "..."
        print
        print "Specify molecules to plot against one another in the following format:"
        print "Plot <Reactant1> vs. <Reactant2>, <Reactant1> vs. <Time> ..."
        exit(0)

    elif args.interactive:
        #Welcome output
        print "****************************"
        print "******Welcome to CASS!******"
        print "****************************"
        print "-This stochastic simulator is useful for modeling biochemical networks."
        print "-Make sure your file is in the correct format (See Documentation)"
        print "-Verify that the file is in the current working directory\n"

        #Try to open data file
        fileOK = False
        while not fileOK:
            try:
                print "Please enter your text file name/path:",
                fileName = str(raw_input())
                dataFile = open(fileName)
                fileOK = True
            except IOError:
                try:
                    dataFile = open(fileName + ".txt")
                    fileOK = True
                except IOError:
                    print "Error - File does not exist"

        #Calls parser        
        equations, moleCounts, duration, max_iterations, output_freq, plots, seed, error = CASSparser.parseText(dataFile.readlines())

        #If error, display and exit
        if error != None:
            print error
            print
            print "The program will now exit."
            exit(1)
        
        #Override file specifications based on input arguments
        if args.no_graphs:
            plots = None
        if args.output_freq > 0:
            output_freq = args.output_freq
        if args.max_iters > 0:
            max_iterations = args.max_iters
        if args.duration > 0:
            duration = args.duration
        if args.seed != None:
            seed = args.seed

        #Calls processor
        fileHandles, molCounts, molVSList, suffix = CASSprocessor.updateAll(equations, moleCounts, duration, max_iterations, output_freq, plots, seed, args.silent)

        #Graphs results
        CASSoutput.graphResults(fileHandles, molCounts, molVSList, suffix)

    elif args.file != None:
        #Try to open data file
        try:
            dataFile = open(args.file)
        except IOError:
            try:
                dataFile = open(args.file + ".txt")
            except IOError:
                print "Error - File does not exist."
                exit(1)

        #Calls parser        
        equations, moleCounts, duration, max_iterations, output_freq, plots, seed, error = CASSparser.parseText(dataFile.readlines())
        print equations
        print moleCounts
        print duration
        print max_iterations
        print output_freq
        print plots
        print seed
        print error

        #If error, display and exit
        if error != None:
            print error
            print
            print "The program will now exit."
            exit(1)

        #Override file specifications based on input arguments
        if args.no_graphs:
            plots = None
        if args.output_freq > 0:
            output_freq = args.output_freq
        if args.max_iters > 0:
            max_iterations = args.max_iters
        if args.duration > 0:
            duration = args.duration
        if args.seed != None:
            seed = args.seed
        
        #Calls processor
        fileHandles, molCounts, molVSList, suffix = CASSprocessor.updateAll(equations, moleCounts, duration, max_iterations, output_freq, plots, seed, args.silent)

        #Graphs results
        CASSoutput.graphResults(fileHandles, molCounts, molVSList, suffix)

    else:
        CASSgui.main()

main()
