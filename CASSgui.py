import CASSparser, CASSprocessor, CASSoutput

from Tkinter import *
import tkFileDialog
import sys, os.path, os

import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

#TO_DO: Add About CASS and CASS Help pages

class Application(Frame):
    #top level frame containing everything
    
    def createWidgets(self):
        #contains an input box on the left containing fields, and an output box on the right containing the graph
        self.mainMenu = menuBar(self.master)
        self.inputBox = variableInput(self.duration, self.maxIterations, self.outputFreq, self.molVSList, self.moleculeText, self.reactionText, self)
        self.inputBox.pack(side = "left", fill=Y)
        
        self.outputBox = dataOutput(self.duration, self.maxIterations, self.rxnsAndMolCounts, self.tupleInputs,
                               self.molCounts, self.outputFreq, self.molVSList, self.moleculeText, self.reactionText, self.graph, self)
        self.outputBox.pack(side = "right", padx = 10)
        
    def __init__(self, duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, version, master=None):
        Frame.__init__(self, master, padx = 5, pady = 5)
        self.master = master
        master.title("Computational Adaptable Stochastic Simulator")
        self.pack()

        self.duration = duration
        self.maxIterations = maxIterations
        self.rxnsAndMolCounts = rxnsAndMolCounts
        self.tupleInputs = tupleInputs
        self.molCounts = molCounts
        self.outputFreq = outputFreq
        self.molVSList = molVSList
        self.moleculeText = moleculeText
        self.reactionText = reactionText
        self.graph = graph
        self.version = version
        
        self.createWidgets()

class variableInput(Frame):
    #leftmost pane of GUI
    
    def createWidgets(self):
        #creates 3 input sections, one for various datapoints like duration, one for the molcounts, and one for the reactions
        self.parametersBox = parameters(self.duration, self.maxIterations, self.outputFreq, self)
        self.parametersBox.grid(row = 0, column = 0, sticky = "WE")

        self.moleculesBox = molecules(self.moleculeText, self)
        self.moleculesBox.grid(row = 1, column = 0)

        self.reactionsBox = reactions(self.reactionText, self)
        self.reactionsBox.grid(row = 2, column = 0)
        
    def __init__(self, duration, maxIterations, outputFreq, molVSList, moleculeText, reactionText, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        self.duration = duration
        self.maxIterations = maxIterations
        self.outputFreq = outputFreq
        self.molVSList = molVSList
        self.moleculeText = moleculeText
        self.reactionText = reactionText
        
        self.createWidgets()

class dataOutput(Frame):
    #rightmost pane of GUI
    
    def createWidgets(self):
        #creates 3 sections, one that displays the graph, one that displays analysis box, and one that allows the user to run the program
        self.runBox = runControl(self.duration, self.maxIterations, self.rxnsAndMolCounts, self.tupleInputs,
                               self.molCounts, self.outputFreq, self.molVSList, self.moleculeText, self.reactionText, self.graph, self)
        self.runBox.grid(row = 1, column = 0, sticky = "WE")

        self.analysisBox = analysis(self)
        self.analysisBox.grid(row = 2, column = 0, sticky = "WES")

        self.graphBox = graphDisplay(self.graph, self)
        self.graphBox.grid(row=0, column = 0, sticky = "WEN")
    
    def __init__(self, duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        self.duration = duration
        self.maxIterations = maxIterations
        self.rxnsAndMolCounts = rxnsAndMolCounts
        self.tupleInputs = tupleInputs
        self.molCounts = molCounts
        self.outputFreq = outputFreq
        self.molVSList = molVSList
        self.moleculeText = moleculeText
        self.reactionText = reactionText
        self.graph = graph
        
        self.createWidgets()

class parameters(LabelFrame):
    #allows the user to input iterations, duration, output frequency, and plotted variables and pass them to the master
    
    def createWidgets(self):
        #creates 3 fields, one for maximum iterations, one for duration, and one for output frequency
        self.iterationsLabel = Label(self, text = "Iterations:")
        self.iterationsLabel.grid(row = 0, column = 0, sticky = 'W')

        self.durationLabel = Label(self, text = "Duration:")
        self.durationLabel.grid(row = 1, column = 0, sticky = 'W')

        self.outputFreqLabel = Label(self, text = "Output Frequency:")
        self.outputFreqLabel.grid(row = 2, column = 0, sticky = 'W')

        self.iterationsEntry = Entry(self, width = 20)
        self.iterationsEntry.insert(0, 1000000)
        self.iterationsEntry.grid(row = 0, column = 1)

        self.durationEntry = Entry(self, width = 20)
        self.durationEntry.insert(0, 30)
        self.durationEntry.grid(row = 1, column = 1)

        self.outputFreqEntry = Entry(self, width = 20)
        self.outputFreqEntry.insert(0, 1000)
        self.outputFreqEntry.grid(row = 2, column = 1)

    def __init__(self, duration, maxIterations, outputFreq, master=None):
        LabelFrame.__init__(self, master, text = "Parameters", padx = 5, pady = 10)
        self.master = master

        self.duration = duration
        self.maxIterations = maxIterations
        self.outputFreq = outputFreq
        
        self.createWidgets()
        
class molecules(LabelFrame):
    #allows the user to input molecounts and passes them up to the master
        
    def clearMolecules(self, textBox):
        #clears the textbox and updates the data in runBox
        textBox.delete('1.0', 'end')
        self.moleculeText = textBox.get('1.0', 'end')
        self.master.master.outputBox.runBox.moleculeText = self.moleculeText
        
    def createWidgets(self):
        #creates a textbox for the user to enter molcounts
        self.textBox = Text(self, width = 40, height = 10)
        self.textBox.pack()

        #using lambda allows arguments to be passed to method
        self.clearButton = Button(self, text = "Clear", command = lambda: self.clearMolecules(self.textBox))
        self.clearButton.pack(pady = 5, padx = 5, side = "left")
        
    def __init__(self, moleculeText, master=None):
        LabelFrame.__init__(self, master, text = "Molecules", padx = 5)
        self.master = master

        self.moleculeText = moleculeText
        self.createWidgets()

class reactions(LabelFrame):
    #allows the user to input reactions and passes them up to the master

    def clearReactions(self, textBox):
        #clears the textbox and updates the data in runBox
        textBox.delete('1.0', 'end')
        self.reactionText = textBox.get('1.0', 'end')
        self.master.master.outputBox.runBox.reactionText = self.reactionText
        
    def createWidgets(self):
        #creates a textbox for the user to enter reactions
        self.textBox = Text(self, width = 40, height = 10)
        self.textBox.pack()
        
        #using lambda allows arguments to be passed to method
        clearButton = Button(self, text = "Clear", command = lambda: self.clearReactions(self.textBox))
        clearButton.pack(pady = 5, padx = 5, side = "left")
    def __init__(self, reactionText, master=None):
        LabelFrame.__init__(self, master, text = "Reactions", padx = 5)
        self.master = master

        self.reactionText = reactionText
        self.createWidgets()

class variablePicker(Toplevel):
    #allows the user to choose their variables
    
    def submitVariables(self, xAxis, yAxis):
        #creates a molVSList based on the user's selections
        x = xAxis.get()
        y = yAxis.get()
        self.master.molVSList = [(x, y), (y, x)]
        self.destroy()
        
    def createWidgets(self):
        #creates radiobuttons based on the variables that the user inputs
        molListChooserFrame = LabelFrame(self, text = "Choose Variables to Plot", padx = 80)

        #creates two lists to store the radiobuttons
        radioList1 = [0]*len(self.master.molCounts)
        radioList2 = [0]*len(self.master.molCounts)

        #two variables to link to the radiobuttons that determine what should be plotted
        xAxis = StringVar()
        yAxis = StringVar()
        counter = 0
        
        xAxisLabel = Label(molListChooserFrame, text = "X Axis")
        xAxisLabel.grid(row = 0, column = 0)
        yAxisLabel = Label(molListChooserFrame, text = "Y Axis")
        yAxisLabel.grid(row = 0, column = 1)
        
        for key in self.master.molCounts.keys():
            print(counter)
            radioList1[counter] = Radiobutton(molListChooserFrame, text = key, variable = xAxis, value = key)
            radioList1[counter].grid(row = counter+1, column = 0, sticky = 'W')
            radioList2[counter] = Radiobutton(molListChooserFrame, text = key, variable = yAxis, value = key)
            radioList2[counter].grid(row = counter+1, column = 1, sticky = 'W')
            counter+=1

        #adds an extra button to plot the time
        timeRadioButton = Radiobutton(molListChooserFrame, text = "Time", variable = xAxis, value = "time")
        timeRadioButton.grid(row=counter+1, column = 0, sticky = 'W')
        
        submitButton = Button(molListChooserFrame, text = "Submit", command=lambda: self.submitVariables(xAxis, yAxis))
        submitButton.grid(row=counter+2, column = 0, sticky = 'W')
        molListChooserFrame.pack()

        #prevents the window from closing immediately
        self.wait_window(self)
        
    def __init__(self, master=None):
        Toplevel.__init__(self, master)
        self.title("Variable Picker")
        self.master = master
        self.resizable(FALSE, FALSE)
        self.createWidgets()
        
class runControl(LabelFrame):
    #allows the user to input a seed and run the reaction

    def runSimulation(self, graph):
        #parses the inputs and runs the actual reaction
        
        #retrieves data from the entry fields
        self.maxIterations = float(self.master.master.inputBox.parametersBox.iterationsEntry.get())
        self.duration = float(self.master.master.inputBox.parametersBox.durationEntry.get())
        self.outputFreq = float(self.master.master.inputBox.parametersBox.outputFreqEntry.get())
        
        self.master.analysisBox.textBox.config(state=NORMAL)
        self.master.analysisBox.textBox.insert('1.0', "Maximum Iterations:" + str(self.maxIterations)+"\n")
        self.master.analysisBox.textBox.insert('2.0', "Output Frequency:" + str(self.outputFreq)+"\n")
        self.master.analysisBox.textBox.insert('3.0', "Duration:" + str(self.duration)+"\n")
        self.master.analysisBox.textBox.config(state=DISABLED)

        self.moleculeText = self.master.master.inputBox.moleculesBox.textBox.get('1.0', 'end')
        
        self.master.analysisBox.textBox.config(state=NORMAL)
        self.master.analysisBox.textBox.insert('1.0', self.moleculeText)
        self.master.analysisBox.textBox.config(state=DISABLED)

        self.reactionText = self.master.master.inputBox.reactionsBox.textBox.get('1.0', 'end')
        
        self.master.analysisBox.textBox.config(state=NORMAL)
        self.master.analysisBox.textBox.insert('1.0', self.reactionText)
        self.master.analysisBox.textBox.config(state=DISABLED)

        self.seed = int(self.seedEntry.get())

        self.master.analysisBox.textBox.config(state=NORMAL)
        self.master.analysisBox.textBox.insert('1.0', "Seed:"+str(self.seed))
        self.master.analysisBox.textBox.config(state=DISABLED)

        #parses data to retrieve fields to input into processor
        self.rxnsAndMolCounts = (self.reactionText+self.moleculeText).splitlines()
        EqnsNmolCounts = CASSparser.parseText(self.rxnsAndMolCounts)
        self.tupleInputs = EqnsNmolCounts[0]
        self.molCounts = EqnsNmolCounts[1]

        self.top = variablePicker(self)
        
        #Calls processor
        self.master.graphBox.graph = CASSprocessor.updateAll(self.tupleInputs, self.molCounts, self.duration, self.maxIterations, self.outputFreq, self.molVSList, self.seed)
        self.master.analysisBox.textBox.config(state=NORMAL)
        self.master.analysisBox.textBox.insert('1.0', 'Simulation Complete')
        self.master.analysisBox.textBox.config(state=DISABLED)
        self.master.graphBox.destroyWidgets()
        self.master.graphBox.createWidgets()

    def clearSimulation(self):
        self.master.graphBox.graph = Figure(figsize = (5, 4), dpi=100)
        self.master.graphBox.destroyWidgets()
        self.master.graphBox.createWidgets()

    def createWidgets(self):
        self.seedLabel = Label(self, text = "Random Seed:")
        self.seedLabel.grid(row = 0, column = 0)

        self.seedEntry = Entry(self, width = 20)
        self.seedEntry.insert(0, self.seed)
        self.seedEntry.grid(row = 0, column = 1)

        self.runButton = Button(self, text = "Run", command = lambda: self.runSimulation(self.graph))
        self.runButton.grid(row = 1, column = 0, sticky = "W")

        self.clearButton = Button(self, text = "Clear", command = self.clearSimulation)
        self.clearButton.grid(row = 1, column = 0, sticky = "E")
    def __init__(self, duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, master=None):
        LabelFrame.__init__(self, master, text = "Run Control", padx = 5, pady = 5)
        self.master = master

        self.seed = 12341234
        self.duration = duration
        self.maxIterations = maxIterations
        self.rxnsAndMolCounts = rxnsAndMolCounts
        self.tupleInputs = tupleInputs
        self.molCounts = molCounts
        self.outputFreq = outputFreq
        self.molVSList = molVSList
        self.moleculeText = moleculeText
        self.reactionText = reactionText
        self.graph = graph
        
        self.createWidgets()

class graphDisplay(Frame):
    #displays the results of the reaction in graph form
    
    def createWidgets(self):
        #displays the graph by embedding the matplotlib Figure into the GUI
        self.frame = Frame(self)
        self.frame.pack()
        self.canvas = FigureCanvasTkAgg(self.graph, master=self.frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side="top", fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side="top", fill=BOTH, expand=1)
    def destroyWidgets(self):
        #destroys the graph so it can be redrawn
        self.frame.destroy()
    def __init__(self, graph, master=None):
        Frame.__init__(self, master)
        self.master = master
        
        self.graph = graph
        self.createWidgets()
        
class analysis(LabelFrame):
    #outputs text such as error messages
    
    def createWidgets(self):
        self.textBox = Text(self, width = 60, height = 5)
        self.textBox.config(state = DISABLED)
        self.textBox.pack()
    def __init__(self, master=None):
        LabelFrame.__init__(self, master, text = "Analysis", padx = 5, pady = 5)
        self.master = master
        
        self.createWidgets()

class menuBar(Menu):
    def askFile(self):
        #allows the user to enter a premade text file to fill out the forms
        filename = tkFileDialog.askopenfilename()
        file = open(filename, 'r')
        strList = file.readlines()
        index = 0
        reactionText = ""
        moleculeText = ""

        #This determines the parameters, reactions, and molecule counts
        #cycles through unimportant text until it finds the reactions
        while("Reactions" not in strList[index]):
            index+=1
        #upon reaching the '#', stops storing for reactionText
        while("#" not in strList[index+1]):
            index+=1
            reactionText = reactionText+strList[index]
        #cycles through unimportant text until it finds the molecule counts
        while("Molecule Count" not in strList[index]):
            index+=1
        #upon reaching the '#', stops storing for moleculeText
        while("#" not in strList[index+1]):
            index+=1
            moleculeText = moleculeText+strList[index]

        #default values for parameters
        duration = 30
        maxIterations = 1000000
        outputFreq=1000
        seed = 12341234

        optionalParams=[]
        #cycles through unimportant text until it finds the optional parameters
        while("Optional Parameters" not in strList[index]):
            index+=1
        #upon reaching the end of the list, stops storing for optionalParams and begins to strip its contents
        while(index<len(strList)-1):
            index+=1
            optionalParams.append(strList[index])
        #strips through the optional params in order to find the values of the parameters
        for i in range(4):
            for s in optionalParams[i].split('='):
                if (s.strip()).isdigit():
                    value = int(s)
                    if(i==0):
                        duration=value
                    if(i==1):
                        maxIterations=value
                    if(i==2):
                        outputFreq=value
                    if(i==3):
                        seed = value
                    break
        #sets the forms to equal the parameters and text that it found
        self.master.app.inputBox.parametersBox.durationEntry.delete(0, 'end')
        self.master.app.inputBox.parametersBox.iterationsEntry.delete(0, 'end')
        self.master.app.inputBox.parametersBox.outputFreqEntry.delete(0, 'end')
        self.master.app.inputBox.reactionsBox.textBox.delete('1.0', 'end')
        self.master.app.inputBox.moleculesBox.textBox.delete('1.0', 'end')
        self.master.app.inputBox.parametersBox.durationEntry.insert(0, duration)
        self.master.app.inputBox.parametersBox.iterationsEntry.insert(0, maxIterations)
        self.master.app.inputBox.parametersBox.outputFreqEntry.insert(0, outputFreq)
        self.master.app.inputBox.reactionsBox.textBox.insert('1.0', reactionText)
        self.master.app.inputBox.moleculesBox.textBox.insert('1.0', moleculeText)

    def saveFile(self):
        filename = tkFileDialog.asksaveasfile(mode='a')
        duration = self.master.app.inputBox.parametersBox.durationEntry.get()
        maxIterations = self.master.app.inputBox.parametersBox.iterationsEntry.get()
        outputFreq = self.master.app.inputBox.parametersBox.outputFreqEntry.get()
        reactionText = self.master.app.inputBox.reactionsBox.textBox.get('1.0', 'end')
        moleculeText = self.master.app.inputBox.moleculesBox.textBox.get('1.0', 'end')
        seed = str(self.master.app.outputBox.runBox.seedEntry.get())

        saveText = "#Reactions\n"+reactionText+"\n#Molecule Count of Reactants\n"+moleculeText+"\n#Optional Parameters\n"+"duration="+duration+"\nmax_iterations="+maxIterations+"\noutput_freq="+outputFreq+"\nseed="+seed
        filename.write(saveText)
    def createWidgets(self):
        self.fileMenu = Menu(self, tearoff=0)
        self.fileMenu.add_command(label = "Open", command = self.askFile)
        self.fileMenu.add_command(label = "Save", command = self.saveFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label = "Exit", command = root.destroy)
        self.add_cascade(label = "File", menu = self.fileMenu)

        self.helpMenu = Menu(self, tearoff = 0)
        self.helpMenu.add_command(label = "About CASS")
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label = "CASS Help")
        self.add_cascade(label = "Help", menu = self.helpMenu)
        
        self.master.config(menu=self)
    def __init__(self, master):
        Menu.__init__(self, master)
        self.master = master
        self.createWidgets()
        
root = Tk()
root.resizable(FALSE, FALSE)
#default values
duration = 30.0
maxIterations = 1000000
rxnsAndMolCounts = ""
tupleInputs = tuple()
molCounts = tuple()
outputFreq = 1000
molVSList = []
moleculeText = ""
reactionText = ""
graph = Figure(figsize = (5, 4), dpi=100)
version = 1.0

root.app = Application(duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, version, master=root)
root.app.mainloop()
