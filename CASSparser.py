#Import regular expression library and sys for exit()
import re, sys, math, numpy, pylab, ast
import random as rng

#Exception that is raised when an error is found during parsing
class ParsingSyntaxError(Exception):
    def __init__(self, string):
        #Print error message
        print string
        print
        print "The program will now exit."
        sys.exit(1)

#Check if all characters are matched
def notAllMatched(inputString, matches):
    found = [False]*len(inputString)
    allFound = []
    for match in matches:
        for i in range(match.start(), match.end()):
            found[i] = True
    i = 0
    while i < len(found):
        characterThere = found[i]
        if not characterThere:
            startPos = i
            while (not characterThere) and (i < len(found)):
                characterThere = found[i]
                i+=1
            endPos = i
            errorString = inputString[startPos:endPos]
            allFound.append([startPos, endPos, errorString])
        i+=1
    return allFound           
    
#Text parsing function
def parseText(inputStrings):
    #Define lists and dictionaries we want to return
    moleCounts = {}
    equations = []
    duration = 100
    max_iterations = 1000000
    output_freq = 10000
    plots = []
    
    #Regular expressions to parse equations
    regExpEqPlus = """
    \s*                             #Ignore leading whitespaces
    (\d*)                           #Find integers
    \s*                             #Ignore whitespaces
    ([^\s\+>\-\[]+)                 #Read characters as word until non-internal digit, whitespace or symbol (+,-,=,>)
    \s*                             #Ignore whitespaces
    \+                              #Find +
    """
    regExpEqArrow = """
    \s*                             #Ignore leading whitespaces
    (\d*)                           #Find integers
    \s*                             #Ignore whitespaces
    ([^\s\+>\-\[]+)                 #Read characters as word until non-internal digit, whitespace or symbol ([,+,-,=,>)
    \s*                             #Ignore whitespaces
    \->                             #Find arrow
    """
    regExpEqEnd = """
    \s*                             #Ignore leading whitespaces
    (\d*)                           #Find integers
    \s*                             #Ignore whitespaces
    ([^\s\+>\-\[]+)                 #Read characters as word until space or open bracket
    \s*                             #Ignore whitespaces
    \[                              #Find open bracket
    """
    regExpEqConstant = """
    \s*                             #Ignore leading whitespaces
    \[                              #Find open brackets
    \s*                             #Ignore whitespaces
    ([\d\.\-]*)                     #Find numbers
    \s*                             #Ignore whitespaces
    \]                              #Find close brackets
    \s*                             #Ignore trailing whitespaces
    """
    regExpDeclaration = """
    \s*                             #Ignore leading whitespaces
    ([^\s\+>\-]+)                   #Read characters as word until non-internal digit, whitespace or symbol (+,-,=,>)
    \s*                             #Ignore whitespaces
    =                               #Find equal sign
    \s*                             #Ignore whitespaces
    ([^\s]+)                        #Find integers
    \s*                             #Ignore trailing whitespaces
    """
    regExpPlot = """
    \s*                             #Ignore leading whitespaces
    plot                            #Find plot (not case-sensitive)
    """
    regExpPlotArgs = """
    \s*                             #Ignore leading whitespaces
    ([^\s]+)                        #Read characters as word until space
    \s*                             #Ignore whitespaces
    vs\.                            #Find vs.
    \s*                             #Ignore whitespaces
    ([^\s,]+)                       #Read characters as word until space or comma
    \s*                             #Ignore trailing whitespaces
    ,?
    \s*
    """

    #Remove exclusively newline character lines
    inputStrings = filter(lambda a: a != "\n", inputStrings)
    
    for i, line in enumerate(inputStrings):
        #If line is a comment or a blank line, ignore it
        if re.match("#", line) or re.search("\S", line) == None:
            continue
        
        #Define outputs
        reactants = {}
        products = {}
        netChange = {}
        moleCount = 0
        constant = 0
        
        #Put all regex matches in a list
        eqPlusMatches = list(re.finditer(regExpEqPlus, line, re.VERBOSE))
        eqArrowMatches = list(re.finditer(regExpEqArrow, line, re.VERBOSE))
        eqEndMatches = list(re.finditer(regExpEqEnd, line, re.VERBOSE))
        eqConstantMatches = list(re.finditer(regExpEqConstant, line, re.VERBOSE))
        declarationMatches = list(re.finditer(regExpDeclaration, line, re.VERBOSE))
        plotMatches = list(re.finditer(regExpPlot, line, re.VERBOSE|re.IGNORECASE))
        plotArgsMatches = list(re.finditer(regExpPlotArgs, line, re.VERBOSE))

        #for match in eqPlusMatches + eqArrowMatches + eqEndMatches + eqConstantMatches + declarationMatches + plotMatches + plotArgsMatches:
        #for match in eqArrowMatches + eqConstantMatches:
        #    print match.groups(), match.start(), match.end()
        #print len(eqArrowMatches)
        #print len(eqConstantMatches)

        #Check for errors
        if len(eqArrowMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one arrow in line " + str(i) + ":\n" + line)        
        if len(eqEndMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one equation terminator in line (you may be missing a '+') " + str(i) + ":\n" + line)
        if len(eqConstantMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one reaction constant in line " + str(i) + ":\n" + line)
        if len(declarationMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one equal sign in line " + str(i) + ":\n" + line)
        if len(plotMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one PLOT command in line " + str(i) + ":\n" + line)
        
        #Figure out whether the line is a reaction, molecule count or plot
        lineType = ""
        print len(plotMatches), len(plotArgsMatches)
        if len(plotMatches) == 1 and len(plotArgsMatches) >= 1:
            lineType = "plot"
        if len(eqConstantMatches) == 1 and len(eqArrowMatches) == 1:
            if lineType != "":
                 raise ParsingSyntaxError("ERROR: Ambiguous line type for line " + str(i) + ":\n" + line)
            else:
                lineType = "equation"
        if len(declarationMatches) == 1:
            if lineType != "":
                raise ParsingSyntaxError("ERROR: Ambiguous line type for line " + str(i) + ":\n" + line)
            else:
                lineType = "declaration"
        if lineType == "":
            raise ParsingSyntaxError("ERROR: Could not identify line type for line " + str(i) + ":\n" + line)
                
        #Make sure all characters are matched, otherwise warn the user
        notMatchedData = notAllMatched(line, eqPlusMatches + eqArrowMatches + eqEndMatches + eqConstantMatches + declarationMatches + plotMatches + plotArgsMatches)
        if notMatchedData != None:
            for notMatchedSet in notMatchedData:
                print "WARNING: The parser could not identify the meaning of line " + str(i) + " characters " + str(notMatchedSet[0]) + " through " + str(notMatchedSet[1]) + ":\n" + notMatchedSet[2]
                print "Ignoring error(s)..."
        
        if lineType == "equation":
            #Find the location of the arrow to later split line into reactants and products
            eqSplitter = eqArrowMatches[0].end()
            try:
                #Set the constant equal to the match that was found
                constant = float(eqConstantMatches[0].group(1))
            except ValueError:   
                raise ParsingSyntaxError("ERROR: The parser was unable to read the molecule count in line " + str(i) + ":\n" + line)
            for match in (eqArrowMatches + eqPlusMatches + eqEndMatches):
                #If coefficient is not found, then set it equal to one
                if match.group(1) == '' or match.group(1) == None:
                    coefficient = 1
                else:
                    coefficient = int(match.group(1))
                elementName = match.group(2)
                if match.start() < eqSplitter:
                    if elementName in reactants:
                        reactants[elementName] += coefficient
                    else:
                        products[elementName] = 0
                        reactants[elementName] = coefficient
                elif match.start() >= eqSplitter:
                    if elementName in products and products[elementName] != 0:
                        products[elementName] += coefficient
                    else:
                        if not elementName in reactants:
                            reactants[elementName] = 0
                        products[elementName] = coefficient
            for reactant in reactants.keys():
                netChange[reactant] = products[reactant] - reactants[reactant]
            equations.append((constant, reactants, netChange))
        elif lineType == "declaration":
            try:
                moleCount = float(declarationMatches[0].group(2))
            except ValueError as e:
                raise ParsingSyntaxError("ERROR: The parser was unable to read the molecule count in line " + str(i) + ":\n" + line + "The error was: " + e.args[0])
            elementName = declarationMatches[0].group(1)
            if elementName == "duration":
                duration = moleCount
            elif elementName == "max_iterations":
                max_iterations = moleCount
            elif elementName == "output_freq":
                output_freq = moleCount
            else:
                moleCounts[elementName] = moleCount
        elif lineType == "plot":
            for match in plotArgsMatches:
                plots.append([match.group(1), match.group(2)])
    return equations, moleCounts, duration, max_iterations, output_freq, plots
