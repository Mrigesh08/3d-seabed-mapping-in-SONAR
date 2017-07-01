import matplotlib
matplotlib.use('TkAgg')
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from tkinter import *
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename

mat = scipy.io.loadmat('./finalMat.mat')
data = mat['finalMat']
depths=[0 for x in range(193)]
data2 = [[0 for x in range(192)] for y in range(1536)]
for x in range(0,192):
	for y in range(0,1536):
		data2[y][x]=abs(data[y][x])

#print (data[:,:])
def init(self):
    fig = plt.figure(figsize=(6, 10))
    plt.rcParams["figure.figsize"] = 1,90
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    f=plt.imshow(data)
    ax.set_aspect('equal')

    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0.75)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.show()

def selectFileData():
    global filename
    filename=askopenfilename()
    print(filename)
    #Label(ctr_right,text=filename,width=15).grid(column=1, row=5)
    entry_B.insert(END,filename)

def selectFileChirpData():
    global filename2
    filename2=askopenfilename()
    print(filename2)
    #Label(ctr_right,text=filename,width=15).grid(column=1, row=5)
    entry_C.insert(END,filename2)

def getDepths(self):
	i=0
	for y in range(0,192):
		runningAverage=0
		runningAverage=0
		baseDifference=0
		for x in range(600,1500,10):
			for z in range(x,x+10):
				runningAverage=(data2[z][y])/(z-x+1) + runningAverage*((z-x)/(z-x+1))
			if runningAverage<200:
				#print("running average")
				#print(runningAverage)
				#print("depth")
				#print(x)
				depths[i]=x/133
				i=i+1
				break
		
		#print("running average 2")
		#print(runningAverage)
		#print(runningAverage2*1000000000000)
		#print(runningAverage2*1000000000000-runningAverage*1000000000000)
		#runningAverage=(runningAverage+runningAverage2)/2;
	
		#print("y break")
		#print(y)
		#print(" ")
	print(depths)	
			
########################################################################
root = Tk()
root.title('2D image generation for SONAR data')
root.geometry('{}x{}'.format(800, 600))

# create all of the main containers
top_frame = Frame(root, bg='#ddd', width = 450, height=50, pady=3)
center = Frame(root, bg='#ddd', width=350, height=190, padx=3, pady=3)
#btm_frame = Frame(root, bg='white', width = 450, height = 45, pady=3)
#btm_frame2 = Frame(root, bg='lavender', width = 450, height = 60, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")
#btm_frame.grid(row = 3, sticky="ew")
#btm_frame2.grid(row = 4, sticky="ew")

# create the center widgets
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

# ctr_left = Frame(center, bg='blue', width=100, height=190)
ctr_mid = Frame(center, bg='white', width=525, height=190, padx=10, pady=3)
ctr_right = Frame(center, bg='white', width=90, height=190, padx=10, pady=3)

# ctr_left.grid(row=0, column = 0, sticky="ns")
ctr_mid.grid(row=0, column = 1, sticky="ns")
ctr_right.grid(row=0, column = 2, sticky="ns")
# create the widgets for the top frame
#model_label = Label(top_frame, text = 'Model Dimensions')
width_label = Label(ctr_right,background='white', text = 'Rows: ',borderwidth = 5)
length_label = Label(ctr_right,background='white', text = 'Columns:')
height_label = Label(ctr_right,background='white', text = 'Start Point:')
button_b1=Button(ctr_right,text="Generate Plot")
button_b2=Button(ctr_right,text="Browse SONAR File", command=selectFileData)
button_b3=Button(ctr_right,text="Browse Chirp File", command=selectFileChirpData)
entry_W = Entry(ctr_right, background="white")
entry_L = Entry(ctr_right, background="white")
entry_H = Entry(ctr_right, background="white")
entry_B = Entry(ctr_right, background="white")
entry_C = Entry(ctr_right,background="white")
# use e.get() to get the string.
#use int(e.get())to convert to int
# use button_b1.bind('<BUTTON-1>',functionName)
# layout the widgets in the top frame
#model_label.grid(row = 0, columnspan = 3)

width_label.grid(row = 1, column = 0,padx=10, pady=10)
length_label.grid(row = 2, column = 0,padx=10, pady=10)
height_label.grid(row = 3, column = 0,padx=10, pady=10)
button_b1.grid(row = 4, column=0,padx=10, pady=10)
button_b2.grid(row=5,column=0,padx=10,pady=10)
button_b3.grid(row=5,column=1,padx=10,pady=10)
entry_W.grid(row = 1, column = 1)
entry_L.grid(row = 2, column = 1)
entry_H.grid(row = 3, column = 1)
entry_B.grid(row=8,column=0)
entry_C.grid(row=9,column=0)
#############################################################################
def init2(self):
    f=Figure(figsize=(4,6),dpi=100)
    a=f.add_subplot(111)
    t=np.arange(0,192,1)
    datax=[[0,192] for y in range(1536)]
    data2=data[1,:]
    print(datax)
    a.plot(datax,data)
    a=plt.imshow(data)
    canvas=FigureCanvasTkAgg(f,master=ctr_mid)
    canvas.show()
    canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=1)
#############################################################################
##############################################################################
button_b1.bind('<Button-1>',getDepths)
root.mainloop()
