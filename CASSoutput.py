import math, os, numpy, pylab, sys, datetime

def graphResults(fileHandles, molCounts, molVSList, suffix, avgOn=False, silent=False):
    #Initialize lists
    fileNames = []
    figList =[]
    
    if not silent:
        #Print message
        print "*******************"
        print "Generating Plots..."
        print "(This may take a few minutes)"
        print "*******************"

    #Draw each graph
    if(molVSList!=None):
        count = 0
        for i in range(len(molVSList)):
            xN=molVSList[i][0]
            yN=molVSList[i][1]
            j=0
            poly = []
            while("time" in molVSList[i][j]):
                j+=1
            listTime = readInTime("%s.dat"%molVSList[i][j], suffix)
            if("time" in xN.lower()):
                listx=listTime
            else:
                listx=readIn("%s.dat"%xN, suffix) 
            if("time" in yN.lower()):
                listy=listTime
            else:
                listy=readIn("%s.dat"% yN, suffix)
            title1="%s vs. %s"%(yN,xN)
            pylab.title(title1)              
            if(yN.lower()=="time"):
                pylab.plot(listy,listx)
                if avgOn:
                    pylab.plot(listy, avgPlot(listy,listx))
                pylab.xlabel("Time")
                pylab.ylabel("%s"%(xN))
            else:
                pylab.plot(listx,listy)
                if avgOn:
                    pylab.plot(listx, avgPlot(listx,listy))
                pylab.xlabel("%s"%(xN))
                pylab.ylabel("%s"%(yN))
            #Constructs an average curve
            fig = pylab.gcf()
            fig.canvas.set_window_title('Computational Adaptable Stochastic Simulator')   
           
            path = str(os.getcwd()) + "\\Results_" + suffix
            name =("%s_Plot_%s.png"%(title1,suffix))
            fig.savefig(os.path.join(path,name),dpi=100)
            fig.set_size_inches(6, 5)
            figList.append(fig)
            if not silent:
                print "********************"
                print "Simulation Complete - Check Folder for files"
                print "********************"
            return fig
        
#Plots the average
def avgPlot(listx, listy):
    intListX = [int(float(x)) for x in listx]
    intListY = [int(float(y)) for y in listy]
    degree=7
    poly = numpy.polyfit(intListX, intListY, degree, rcond=None, full=False, w=None, cov=False) 
    newY=[]
    for x in range(len(listx)):
        tempY=0.0
        for p in range(len(poly)):
            tempY+=poly[p]*x**(len(poly)-1-p)
        newY.append(tempY)
    return newY

#Reads the created files for plotting (specific for time variable)
def readInTime(fileName, suffix):
    try:
        list1=[]
        path = str(os.getcwd()) + "\\Results_" + suffix
        fileDir=os.path.join(path,fileName)
        file = open(fileDir,"r")
        for line in file.readlines():
            if "Time" not in line:
                list1.append(line.split(" ",1)[0])   
        return list1
    except IOError:
        return []
                
#Reads the created files for plotting
def readIn(fileName, suffix):
    try:
        list1=[]
        path = str(os.getcwd()) + "\\Results_" + suffix
        fileDir=os.path.join(path,fileName)
        file = open(fileDir,"r")
        for line in file.readlines():
            if "Time" not in line:
                list1.append(line.split(" ",1)[1])   
        return list1
    except IOError:
        return []
