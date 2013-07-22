#Import regular expression library and sys for exit()
import re, sys, math, numpy, pylab
import random as rng

teststrings = ['2C + B -> 3B + A [.005]']

#Exception that is raised when an error is found during parsing
class ParsingSyntaxError(Exception):
    def __init__(self, string):
        #Print error message
        print string
        print
        print "The program will now exit."
        sys.exit(1)

#Some working test strings
#testStrings = ['Akash = 0','Akash + 12Darn -> Fub [-1.33]','4B + D -> A [1.44]','C + 3A -> 2B [1.68]','A = 40','B = 20','C = 10','D = 5']

#Text parsing function
def parseText(inputStrings):
    #Define lists and dictionaries we want to return
    moleCounts = {}
    equations = []
    
    #Regular expressions
    regExpEqPlus = """
    (\d*)                           #Find integers
    \s*                             #Ignore whitespaces
    ([^\d\s\+>\-]+)                 #Read characters as word until digit, whitespace or symbol (+,-,=,>)
    \s*                             #Ignore whitespaces
    \+                              #Find +
    """
    regExpEqArrow = """
    (\d*)                           #Find integers
    \s*                             #Ignore whitespaces
    ([^\d\s\+>\-]+)                 #Read characters as word until digit, whitespace or symbol (+,-,=,>)
    \s*                             #Ignore whitespaces
    \->                             #Find arrow
    """
    regExpEqEnd = """
    (\d*)                           #Find integers
    \s*                             #Ignore whitespaces
    ([^\d\s\+>\-]+)                 #Read characters as word until digit, whitespace or symbol (+,-,=,>)
    \s*                             #Ignore whitespaces
    \[                              #Find bracket
    """
    regExpEqConstant = """
    \[                              #Find open brackets
    \s*                             #Ignore whitespaces
    ([\d\.\-]*)                     #Find numbers
    \s*                             #Ignore whitespaces
    \]                              #Find close brackets
    """
    regExpDeclaration = """
    ([^\d\s\+>\-]+)                 #Read characters as word until digit, whitespace or symbol (+,-,=,>)
    \s*                             #Ignore whitespaces
    =                               #Find equal
    \s*                             #Ignore whitespaces
    (\d*)                           #Find integers
    """

    for i, line in enumerate(inputStrings):
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
        
        #Check for errors
        if len(eqArrowMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one arrow in line " + str(i) + ":\n" + line)        
        if len(eqEndMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one equation terminator in line (you may be missing a '+') " + str(i) + ":\n" + line)
        if len(eqConstantMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one reaction constant in line " + str(i) + ":\n" + line)
        if len(declarationMatches) > 1:
            raise ParsingSyntaxError("ERROR: The parser found more than one equal sign in line " + str(i) + ":\n" + line)
        if len(eqArrowMatches) == len(declarationMatches):
            raise ParsingSyntaxError("ERROR: The parser could not determine whether line " + str(i) + " is a molecule-count declaration or reaction equation:\n" + line)

        definitionOrEquation = bool(len(declarationMatches))   #If the line is an definition, lineType will be True. If the line is an equation, lineType will be False.

        if definitionOrEquation == False:   #If the line is an equation
            eqSplitter = eqArrowMatches[0].end()    #Split the line at the first arrow
            #Make sure no more than one reaction constant is specified
            if len(eqConstantMatches) > 1:
                raise ParsingSyntaxError("ERROR: The parser found more than one reaction constant in line " + str(i) + ":\n" + line)
            else:
                constant = float(eqConstantMatches[0].group(1)) #Set the constant equal to the match that was found
            for match in (eqArrowMatches + eqPlusMatches + eqEndMatches):
                #If coefficient is not found, then set it equal to one
                if match.group(1) == '' or match.group(1) == None:
                    coefficient = 1
                else:
                    coefficient = int(match.group(1))
                elementName = match.group(2)
                if match.start() < eqSplitter:
                    if elementName in reactants:
                        raise ParsingSyntaxError("ERROR: The parser found more than one of the same reactant in line " + str(i) + ":\n" + line)
                    else:
                        products[elementName] = 0
                        reactants[elementName] = coefficient
                elif match.start() >= eqSplitter:
                    if elementName in products and products[elementName] != 0:
                            raise ParsingSyntaxError("ERROR: The parser found more than one of the same product in line " + str(i) + ":\n" + line)
                    else:
                        if not elementName in reactants:
                            reactants[elementName] = 0
                        products[elementName] = coefficient
            for reactant in reactants.keys():
                netChange[reactant] = products[reactant] - reactants[reactant]
            equations.append((constant, reactants, netChange))
        else:   #If the line is a definition
            moleCount = int(declarationMatches[0].group(2))
            elementName = declarationMatches[0].group(1)
            moleCounts[elementName] = moleCount
    return equations, moleCounts
        
##equations, moleCounts = parseText(testStrings)
##print equations
##print moleCounts
##''''''

print parseText(teststrings)
