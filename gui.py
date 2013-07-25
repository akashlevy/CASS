from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler


from matplotlib.figure import Figure

class Application(Frame):
    def createWidgets(self):
        inputBox = variableInput(self)
        inputBox.pack(side = "left", fill=Y)
        
        outputBox = dataOutput(self)
        outputBox.pack(side = "right", padx = 10)
        
    def __init__(self, master=None):
        Frame.__init__(self, master, padx = 5, pady = 5)
        self.master = master
        master.title("CASS")
        self.pack()
        self.createWidgets()

class variableInput(Frame):
    def createWidgets(self):
        parametersbox = parameters(self)
        parametersbox.grid(row = 0, column = 0, sticky = "WE")

        moleculesbox = molecules(self)
        moleculesbox.grid(row = 1, column = 0)

        reactionsbox = reactions(self)
        reactionsbox.grid(row = 2, column = 0)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()

class dataOutput(Frame):
    def createWidgets(self):
        runBox = runControl(self)
        runBox.grid(row = 1, column = 0, sticky = "WE")

        analysisBox = analysis(self)
        analysisBox.grid(row = 2, column = 0, sticky = "WES")

        graphBox = graphDisplay(self)
        graphBox.grid(row=0, column = 0, sticky = "WEN")
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()

class parameters(LabelFrame):
    def createWidgets(self):
        iterationsLabel = Label(self, text = "Iterations:")
        iterationsLabel.grid(row = 0, column = 0)
        
        variablesLabel = Label(self, text = "Plotted Variables:")
        variablesLabel.grid(row = 1, column = 0)

        iterationsEntry = Entry(self, width = 20)
        iterationsEntry.grid(row = 0, column = 1)

        variablesEntry = Entry(self, width = 20)
        variablesEntry.grid(row = 1, column = 1)
    def __init__(self, master=None):
        LabelFrame.__init__(self, master, text = "Parameters", padx = 5, pady = 10)
        self.createWidgets()
        
class molecules(LabelFrame):
    def createWidgets(self):
        textBox = Text(self, width = 40, height = 10)
        textBox.pack()

        submitButton = Button(self, text = "Submit")
        submitButton.pack(pady = 5, side = "left")

        clearButton = Button(self, text = "Clear")
        clearButton.pack(pady = 5, padx = 5, side = "left")
    def __init__(self, master=None):
        LabelFrame.__init__(self, master, text = "Molecules", padx = 5)
        self.createWidgets()

class reactions(LabelFrame):
    def createWidgets(self):
        textBox = Text(self, width = 40, height = 10)
        textBox.pack()
        
        submitButton = Button(self, text = "Submit")
        submitButton.pack(pady = 5, side = "left")

        clearButton = Button(self, text = "Clear")
        clearButton.pack(pady = 5, padx = 5, side = "left")
    def __init__(self, master=None):
        LabelFrame.__init__(self, master, text = "Reactions", padx = 5)
        self.createWidgets()

class runControl(LabelFrame):
    def createWidgets(self):
        seedLabel = Label(self, text = "Random Seed:")
        seedLabel.grid(row = 0, column = 0)

        seedEntry = Entry(self, width = 20)
        seedEntry.grid(row = 0, column = 1)

        runButton = Button(self, text = "Run")
        runButton.grid(row = 1, column = 0, sticky = "W")
    def __init__(self, master=None):
        LabelFrame.__init__(self, master, text = "Run Control", padx = 5, pady = 5)
        self.createWidgets()

class graphDisplay(Frame):
    def createWidgets(self):
        f = Figure(figsize=(5,4), dpi=100)
        a = f.add_subplot(111)
        t = arange(0.0,3.0,0.01)
        s = sin(2*pi*t)

        a.plot(t,s)


        # a tk.DrawingArea
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side="top", fill=BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg( canvas, self )
        toolbar.update()
        canvas._tkcanvas.pack(side="top", fill=BOTH, expand=1)
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()
class analysis(LabelFrame):
    def createWidgets(self):
        textBox = Text(self, width = 40, height = 5)
        textBox.config(state = DISABLED)
        textBox.pack()
    def __init__(self, master=None):
        LabelFrame.__init__(self, master, text = "Analysis", padx = 5, pady = 5)
        self.createWidgets()

root = Tk()
app = Application(master=root)
menuBar = Menu(root)

fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label = "Open")
fileMenu.add_command(label = "Save")
fileMenu.add_separator()
fileMenu.add_command(label = "Exit", command = app.quit)
menuBar.add_cascade(label = "File", menu = fileMenu)

helpMenu = Menu(menuBar, tearoff = 0)
helpMenu.add_command(label = "About CASS")
helpMenu.add_separator()
helpMenu.add_command(label = "CASS Help")
menuBar.add_cascade(label = "Help", menu = helpMenu)
root.config(menu=menuBar)
app.mainloop()
