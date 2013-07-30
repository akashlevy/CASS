import CASSparser, CASSprocessor, CASSoutput

from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

#PRIORITY_TO_DO: Add molVSList dialog box
#TO_DO: Add an Open file dialog box
#TO_DO: Add About CASS and CASS Help pages
#TO_DO: Remove submit buttons

class Application(Frame):
    #top level frame containing everything
    
    def createWidgets(self):
        self.inputBox = variableInput(self.duration, self.maxIterations, self.outputFreq, self.molVSList, self.moleculeText, self.reactionText, self)
        self.inputBox.pack(side = "left", fill=Y)
        
        self.outputBox = dataOutput(self.duration, self.maxIterations, self.rxnsAndMolCounts, self.tupleInputs,
                               self.molCounts, self.outputFreq, self.molVSList, self.moleculeText, self.reactionText, self.graph, self)
        self.outputBox.pack(side = "right", padx = 10)
        
    def __init__(self, duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, master=None):
        Frame.__init__(self, master, padx = 5, pady = 5)
        self.master = master
        master.title("CASS")
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
        
        self.createWidgets()

class variableInput(Frame):
    #leftmost pane of GUI
    
    def createWidgets(self):
        self.parametersbox = parameters(self.duration, self.maxIterations, self.outputFreq, self)
        self.parametersbox.grid(row = 0, column = 0, sticky = "WE")

        self.moleculesbox = molecules(self.moleculeText, self)
        self.moleculesbox.grid(row = 1, column = 0)

        self.reactionsbox = reactions(self.reactionText, self)
        self.reactionsbox.grid(row = 2, column = 0)
        
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

    def getInputData(self, iterationsEntry, durationEntry, outputFreqEntry):
        #setting the maxIterations, outputFreq, and duration of the runBox
        self.master.master.outputBox.runBox.maxIterations = float(iterationsEntry.get())
        self.master.master.outputBox.runBox.outputFreq = float(outputFreqEntry.get())
        self.master.master.outputBox.runBox.duration = float(durationEntry.get())

        #setting the text of the analysis box to indicate the change
        self.master.master.outputBox.analysisBox.textBox.config(state=NORMAL)
        self.master.master.outputBox.analysisBox.textBox.insert('1.0', "Maximum Iterations:" + iterationsEntry.get()+"\n")
        self.master.master.outputBox.analysisBox.textBox.insert('2.0', "Output Frequency:" + outputFreqEntry.get()+"\n")
        self.master.master.outputBox.analysisBox.textBox.insert('3.0', "Duration:" + durationEntry.get()+"\n")
        self.master.master.outputBox.analysisBox.textBox.config(state=DISABLED)

    def createWidgets(self):
        self.iterationsLabel = Label(self, text = "Iterations:")
        self.iterationsLabel.grid(row = 0, column = 0, sticky = 'W')

        self.durationLabel = Label(self, text = "Duration:")
        self.durationLabel.grid(row = 1, column = 0, sticky = 'W')

        self.outputFreqLabel = Label(self, text = "Output Frequency:")
        self.outputFreqLabel.grid(row = 2, column = 0, sticky = 'W')

        self.iterationsEntry = Entry(self, width = 20)
        self.iterationsEntry.grid(row = 0, column = 1)

        self.durationEntry = Entry(self, width = 20)
        self.durationEntry.grid(row = 1, column = 1)

        self.outputFreqEntry = Entry(self, width = 20)
        self.outputFreqEntry.grid(row = 2, column = 1)

        self.submitButton = Button(self, text = "Submit", command = lambda: self.getInputData(self.iterationsEntry, self.durationEntry, self.outputFreqEntry))
        self.submitButton.grid(row = 3, column = 0, sticky = 'W')
    def __init__(self, duration, maxIterations, outputFreq, master=None):
        LabelFrame.__init__(self, master, text = "Parameters", padx = 5, pady = 10)
        self.master = master

        self.duration = duration
        self.maxIterations = maxIterations
        self.outputFreq = outputFreq
        
        self.createWidgets()
        
class molecules(LabelFrame):
    #allows the user to input molecounts and passes them up to the master
    
    def submitMolecules(self, textBox):
        self.moleculeText = textBox.get('1.0', 'end')
        #setting the moleculeText of the runBox
        self.master.master.outputBox.runBox.moleculeText = self.moleculeText
        #setting the text of the analysis box to indicate the change
        self.master.master.outputBox.analysisBox.textBox.config(state=NORMAL)
        self.master.master.outputBox.analysisBox.textBox.insert('1.0', self.moleculeText)
        self.master.master.outputBox.analysisBox.textBox.config(state=DISABLED)
        
    def clearMolecules(self, textBox):
        textBox.delete('1.0', 'end')
        self.moleculeText = textBox.get('1.0', 'end')
        self.master.master.outputBox.runBox.moleculeText = self.moleculeText
        
    def createWidgets(self):
        self.textBox = Text(self, width = 40, height = 10)
        self.textBox.pack()

        #using lambda allows arguments to be passed to submitMolecules method
        self.submitButton = Button(self, text = "Submit", command = lambda: self.submitMolecules(self.textBox))
        self.submitButton.pack(pady = 5, side = "left")

        self.clearButton = Button(self, text = "Clear", command = lambda: self.clearMolecules(self.textBox))
        self.clearButton.pack(pady = 5, padx = 5, side = "left")
        
    def __init__(self, moleculeText, master=None):
        LabelFrame.__init__(self, master, text = "Molecules", padx = 5)
        self.master = master

        self.moleculeText = moleculeText
        self.createWidgets()

class reactions(LabelFrame):
    #allows the user to input reactions and passes them up to the master
    
    def submitReactions(self, textBox):
        self.reactionText = textBox.get('1.0', 'end')
        #setting the reactionText of the runBox
        self.master.master.outputBox.runBox.reactionText = self.reactionText
        #setting the text of the analysis box to indicate the change
        self.master.master.outputBox.analysisBox.textBox.config(state=NORMAL)
        self.master.master.outputBox.analysisBox.textBox.insert('1.0', self.reactionText)
        self.master.master.outputBox.analysisBox.textBox.config(state=DISABLED)

    def clearReactions(self, textBox):
        textBox.delete('1.0', 'end')
        self.reactionText = textBox.get('1.0', 'end')
        self.master.master.outputBox.runBox.reactionText = self.reactionText
        
    def createWidgets(self):
        self.textBox = Text(self, width = 40, height = 10)
        self.textBox.pack()
        
        self.submitButton = Button(self, text = "Submit", command = lambda: self.submitReactions(self.textBox))
        self.submitButton.pack(pady = 5, side = "left")

        clearButton = Button(self, text = "Clear", command = lambda: self.clearReactions(self.textBox))
        clearButton.pack(pady = 5, padx = 5, side = "left")
    def __init__(self, reactionText, master=None):
        LabelFrame.__init__(self, master, text = "Reactions", padx = 5)
        self.master = master

        self.reactionText = reactionText
        self.createWidgets()

class runControl(LabelFrame):
    #allows the user to input a seed and run the reaction

    def runSimulation(self, duration, maxIterations, rxnsAndMolCounts, tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph):
        #parses the inputs and runs the actual reaction
        rxnsAndMolCounts = (reactionText+moleculeText).splitlines()
        print(rxnsAndMolCounts)
        EqnsNmolCounts = CASSparser.parseText(rxnsAndMolCounts)
        tupleInputs = EqnsNmolCounts[0]
        print(tupleInputs)
        molCounts = EqnsNmolCounts[1]
        print(molCounts)
        #temporary hardcoding, will need to change later
        molVSList = [('R', 'W'), ('W', 'R')] #############################################
        
        #Calls processor
        self.master.graphBox.graph = CASSprocessor.updateAll(tupleInputs, molCounts, duration, maxIterations, outputFreq, molVSList)
        self.master.graphBox.destroyWidgets()
        self.master.graphBox.createWidgets()

    def createWidgets(self):
        self.seedLabel = Label(self, text = "Random Seed:")
        self.seedLabel.grid(row = 0, column = 0)

        self.seedEntry = Entry(self, width = 20)
        self.seedEntry.grid(row = 0, column = 1)

        self.runButton = Button(self, text = "Run", command = lambda: self.runSimulation(self.duration, self.maxIterations, self.rxnsAndMolCounts, self.tupleInputs,
                                                                                    self.molCounts, self.outputFreq, self.molVSList, self.moleculeText,
                                                                                    self.reactionText, self.graph))
        self.runButton.grid(row = 1, column = 0, sticky = "W")
    def __init__(self, duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, master=None):
        LabelFrame.__init__(self, master, text = "Run Control", padx = 5, pady = 5)
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

class graphDisplay(Frame):
    #displays the results of the reaction in graph form
    
    def createWidgets(self):
        self.frame = Frame(self)
        self.frame.pack()
        self.canvas = FigureCanvasTkAgg(self.graph, master=self.frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side="top", fill=BOTH, expand=1)

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side="top", fill=BOTH, expand=1)
    def destroyWidgets(self):
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

app = Application(duration, maxIterations, rxnsAndMolCounts,
                  tupleInputs, molCounts, outputFreq, molVSList, moleculeText, reactionText, graph, master=root)

#creates the menu bar
menuBar = Menu(root)

fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label = "Open")
fileMenu.add_command(label = "Save")
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = root.destroy)
menuBar.add_cascade(label = "File", menu = fileMenu)

helpMenu = Menu(menuBar, tearoff = 0)
helpMenu.add_command(label = "About CASS")
helpMenu.add_separator()
helpMenu.add_command(label = "CASS Help")
menuBar.add_cascade(label = "Help", menu = helpMenu)
root.config(menu=menuBar)

app.mainloop()
