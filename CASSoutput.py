import math, os, numpy, pylab, sys, datetime

def graphResults(fileHandles, molCounts, molVSList, suffix):
    fileNames = []
    if(molVSList!=None):
        count=0
        for i in range(len(molVSList)):
            xN=molVSList[i][0]
            yN=molVSList[i][1]
            j=0
            while("time" in molVSList[i][j]):
                j+=1
            listTime=readInTime("%s.dat"%molVSList[i][j], suffix)
            if("time" in xN.lower()):
                listx=listTime
            else:
                listx=readIn("%s.dat"%xN, suffix) 
            if("time" in yN.lower()):
                listy=listTime
            else:
                listy=readIn("%s.dat"% yN, suffix)
            title1="%s vs. %s"%(xN,yN)
            pylab.title(title1)
            if(yN.lower()=="time"):
                pylab.plot(listy,listx)
                pylab.xlabel("Time")
                pylab.ylabel("%s Population"%(xN))
            else:
                pylab.plot(listx,listy)
                pylab.xlabel("%s Population"%(xN))
                pylab.ylabel("%s Population"%(yN))
            fig = pylab.gcf()
            fig.canvas.set_window_title('Computational Adaptable Stochastic Simulator')
            path = str(os.getcwd()) + "\\Results_" + suffix
            name =("%s_Plot_%s.png"%(title1,suffix))
            fig.savefig(os.path.join(path,name), dpi=100)
            fig.set_size_inches(6, 5)
            return fig
            
#Reads the created files for plotting (specific for time variable)
def readInTime(fileName, suffix):
    list1=[]
    path = str(os.getcwd()) + "\\Results_" + suffix
    fileDir=os.path.join(path,fileName)
    file = open(fileDir,"r")
    for line in file.readlines():
        if "Time" not in line:
            list1.append(line.split(" ",1)[0])   
    return list1
                
#Reads the created files for plotting
def readIn(fileName, suffix):
    list1=[]
    path = str(os.getcwd()) + "\\Results_" + suffix
    fileDir=os.path.join(path,fileName)
    file = open(fileDir,"r")
    for line in file.readlines():
        if "Time" not in line:
            list1.append(line.split(" ",1)[1])   
    return list1
