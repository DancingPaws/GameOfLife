from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import math
import random
import os.path

win = Tk()

sideLength=10 #num of cells in row/column
scaleFactor=80 #scale cell only for visual representation
density=0
array=np.zeros((sideLength,sideLength))
convolutionMatrix=np.array([[1,1,1],[1,0,1],[1,1,1]])
generationsDensity=[]
generationsAll=0
path="D:/Uni/GoL/Results/100x100_0.3/" #change path  40x40_0.3/

def changeGrid():
    global sideLength
    global scaleFactor
    global array
    global generationsDensity
    global generationsAll
    global density
    if(0<int(entryNumberOfCells.get())<=100):
        generationsDensity=[]
        density=0
        generationsAll=0
        sideLength=int(entryNumberOfCells.get())
        scaleFactor=int(800/sideLength)
        array=np.zeros((sideLength,sideLength))
        info()
        grid()
    else:
        messagebox.showerror(title="Error", message="Please, input a number between 0 and 100.")


def savePattern():
    num=0
    patt="pattern_" + str(sideLength) + "x" + str(sideLength) + "_" + str(density) + "_"  + str(num) + ".txt"
    pp=path + patt
    while(os.path.exists(pp)):
        num+=1
        patt="pattern_" + str(sideLength) + "x" + str(sideLength) + "_" + str(density) + "_" + str(num) + ".txt"
        pp=path + patt
    with open(pp,"w+") as file:
        for y in range(0,sideLength):
            for x in range(0,sideLength):
                file.write(str(int(array[x,y])))
            file.write("\n")
    
def loadPattern():
    global sideLength
    global scaleFactor
    global array
    global density
    global generationsDensity
    global generationsAll
    generationsDensity=[]
    pattern = filedialog.askopenfilename( initialdir=path, title="Select pattern", filetypes=(("text files", "*.txt"), ("all files", "*.*")))  
    sideLength = sum(1 for line in open(pattern))
    scaleFactor = math.floor(800 / sideLength)
    array=np.zeros((sideLength,sideLength))
    with open(pattern,"r") as file:
        for x in range(0,sideLength):
            for y in range(0,sideLength):
                array[y,x]=file.read(1)
            file.read(1)
    density = np.sum(array/(sideLength*sideLength))
    generationsAll=0
    info()
    grid()
    draw()
    
def saveDensity():
    global generationsDensity 
    num=0
    den="density_" + str(sideLength) + "x" + str(sideLength) + "_" + str(density) + "_" + str(num) + ".txt"
    pd=path + den
    while(os.path.exists(pd)):
        num+=1
        den="density_" + str(sideLength) + "x" + str(sideLength) + "_" + str(density) + "_" + str(num) + ".txt"
        pd=path + den
    with open(pd,"w+") as file:
        for num in range(0,len(generationsDensity)):
            file.write("{:.4f}".format(round(generationsDensity[num], 4)))
            file.write("\n")

def generate():
    global array
    global generationsDensity
    global generationsAll
    global density
    generationsDensity=[]
    if d.get() == 0:
        try:
            density = float(entryDensity.get()) 
        except:
            messagebox.showerror(title="Error", message="Please, input a number between 0 and 1.")
            return   
    else:
        density = d.get()*0.1
    numOfLiveCells=int(sideLength**2*density)
    array=np.zeros((sideLength,sideLength))
    #random fill with 1
    for position in random.sample(range(sideLength**2), numOfLiveCells):
        array[position//sideLength][position%sideLength] = 1
    array = array.astype(int)
    #print(array) 
    density = np.sum(array/(sideLength*sideLength))
    generationsAll=0
    info() 
    grid()
    draw()    

def generations():
    global array
    global density
    global generationsDensity
    global generationsAll
    arrayOfArrays=np.array([array])
    if g.get() == 100:
        repetitions = int(entryGenerations.get())
    elif g.get() == 0:
        repetitions = -1  
    else:
        repetitions = g.get()
    while(repetitions==-1 or repetitions>0):
        newArray=np.zeros((sideLength,sideLength))
        neighboursArray=np.zeros((sideLength,sideLength))
        for x in range(0,sideLength):
            for y in range(0,sideLength):
                xPrew = x-1
                xNext = x+1
                yPrew = y-1
                yNext = y+1
                #periodic boundary
                if(x==0):
                    xPrew = sideLength-1
                if(x==sideLength-1):
                    xNext = 0
                if(y==0):
                    yPrew = sideLength-1
                if(y==sideLength-1):
                    yNext = 0           
                segment = np.array([[array[xPrew,yPrew],array[x,yPrew],array[xNext,yPrew]],
                                    [array[xPrew,y],array[x,y],array[xNext,y]],
                                    [array[xPrew,yNext],array[x,yNext],array[xNext,yNext]]])
                #in every cell is the number of cells neighbours
                neighboursArray[x,y] = np.sum(np.multiply(segment,convolutionMatrix))
        #apply specific rules for GoL
        for x in range(0,sideLength):
            for y in range(0,sideLength):
                if(array[x,y]==1 and (2<=neighboursArray[x,y]<=3)):
                    newArray[x,y]=1
                elif(array[x,y]==0 and neighboursArray[x,y]==3):
                    newArray[x,y]=1        
        if(repetitions>0):
            repetitions=repetitions-1        
        elif(repetitions==-1):
            #generationsDensity
            if(np.sum(array)==0 or np.array_equal(newArray,array)):  #check if no alive cells or for repeating last pattern          
                repetitions=0 
            elif(repetitions!=0):
                for a in range(0,np.shape(arrayOfArrays)[0]): 
                    if(np.array_equal(arrayOfArrays[a],newArray)):
                        repetitions=0 
                        break  
                arrayOfArrays= np.concatenate((arrayOfArrays, [newArray]))      
        array=newArray
        density = np.sum(array/(sideLength*sideLength))
        generationsDensity.append(density)
        generationsAll=generationsAll+1
    info()
    grid()
    draw() 

def click(event):
    global array
    global density
    global generationsDensity
    global generationsAll
    generationsDensity=[]
    generationsAll=0
    x=int(event.x/scaleFactor)
    y=int(event.y/scaleFactor)
    if(array[x,y]==1):
        array[x,y]=0
    else:
        array[x,y]=1
    density = np.sum(array/(sideLength*sideLength))
    info()
    grid()
    draw()

def info():
    ll.set(str(generationsAll))        
    l.set("{:.4f}".format(round(density, 4)))

def grid():
    canvas.delete("all")
    for x in range(0,sideLength+1):
        canvas.create_line(0, x*scaleFactor, sideLength*scaleFactor, x*scaleFactor, fill="#909090")
        canvas.create_line(x*scaleFactor, 0, x*scaleFactor, sideLength*scaleFactor, fill="#909090")

def draw():
    for x in range(0,sideLength):
        for y in range(0,sideLength):
            if(array[x,y]==1):
                canvas.create_oval(x*scaleFactor, y*scaleFactor, (x+1)*scaleFactor, (y+1)*scaleFactor, fill="#303030")

canvas = Canvas(win, bg="white", width=sideLength*scaleFactor, height=sideLength*scaleFactor)
canvas.grid(row = 0, column=0, rowspan=14, sticky=W)
canvas.bind("<Button-1>", click)
grid()

d = IntVar()
lfDen = LabelFrame(win, text="Density")
lfDen.grid(row=0, column=1, rowspan=4, columnspan=2, sticky='W', padx=30, pady=5, ipadx=5, ipady=5)
Radiobutton(lfDen, text="0.3", padx = 20, variable=d, value=3).grid(row=1, column=0, columnspan=2, sticky=W)
Radiobutton(lfDen, text="0.5", padx = 20, variable=d, value=5).grid(row=2, column=0, columnspan=2, sticky=W)
Radiobutton(lfDen, text="0.7", padx = 20, variable=d, value=7).grid(row=3, column=0, columnspan=2, sticky=W)
Radiobutton(lfDen, text="Other:", padx = 20, variable=d, value=0).grid(row=4, column=0, columnspan=1, sticky=W)
entryDensity = Entry(lfDen, width=12)
entryDensity.grid(row=4, column=1, sticky=W)

g = IntVar()
lfGen = LabelFrame(win, text="Generations")
lfGen.grid(row=3, column=1, rowspan=4, columnspan=2, sticky='W', padx=30, pady=5, ipadx=5, ipady=5)
Radiobutton(lfGen, text="1", padx = 20, variable=g, value=1).grid(row=1, column=0, columnspan=2, sticky=W)
Radiobutton(lfGen, text="10", padx = 20, variable=g, value=10).grid(row=2, column=0, columnspan=2, sticky=W)
Radiobutton(lfGen, text="Stabilize", padx = 20, variable=g, value=0).grid(row=3, column=0, columnspan=2, sticky=W)
Radiobutton(lfGen, text="Other:", padx = 20, variable=g, value=100).grid(row=4, column=0, columnspan=1, sticky=W)
entryGenerations = Entry(lfGen, width=12)
entryGenerations.grid(row=4, column=1, sticky=W)

l = StringVar()
ll = StringVar()
lfInf = LabelFrame(win, text="Information")
lfInf.grid(row=6, column=1, rowspan=3, columnspan=2, sticky='W', padx=30, pady=5, ipadx=5, ipady=5)
Label(lfInf, text="Density: ", padx = 20).grid(row=0, column=0, sticky=W)
Label(lfInf, textvariable=l, padx = 20).grid(row=0, column=1, sticky=W)
Label(lfInf, text="Generations: ", padx = 20).grid(row=1, column=0, sticky=W)
Label(lfInf, textvariable=ll, padx = 20).grid(row=1, column=1, sticky=W)

lfNum = LabelFrame(win, text="")
lfNum.grid(row=8, column=1, rowspan=3, columnspan=2, sticky='W', padx=30, pady=5, ipadx=5, ipady=5)
Label(lfNum, text="Cells in a row: ", padx = 20).grid(row=0, column=0, sticky=NW)
entryNumberOfCells = Entry(lfNum, width=6)
entryNumberOfCells.grid(row=0, column=1, sticky=NW)
Button(lfNum, text="Change grid", width=19, height=1, command=changeGrid).grid(row=1, column=0, columnspan=2, sticky=SE)

Button(win, text="Generate Pattern", width=12, command=generate).grid(row=10, column=1, columnspan=1, sticky=S)
Button(win, text="Load Pattern", width=12, command=loadPattern).grid(row=10, column=2, columnspan=1, sticky=S)
Button(win, text="Save Pattern", width=12, command=savePattern).grid(row=11, column=1, columnspan=1)
Button(win, text="Save Densities", width=12, command=saveDensity).grid(row=11, column=2, columnspan=1)
Button(win, text="Generations", width=30, height=2, command=generations).grid(row=12, column=1, columnspan=2, sticky=N)

"""for gsgs in range(0,100):
    generate()
    savePattern()
    generations()
    saveDensity()"""

mainloop()