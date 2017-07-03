import random
from scipy.signal import hilbert
import matplotlib
matplotlib.use('TkAgg')
import scipy.io
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from tkinter import *
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfilename
import plotly as py
import plotly.graph_objs as go
import pandas as pd

py.offline.init_notebook_mode()

#mat = scipy.io.loadmat('./finalMat.mat')
###########################################################################################

###########################################################################################

depths=[0 for x in range(192)]
#data2 = [[0 for x in range(192)] for y in range(1536)]
#for x in range(0,192):
#	for y in range(0,1536):
#		data2[y][x]=abs(finalMat[y][x])
global depthsArr

def generate2DPlot():
	global filename
	global finalMat
	mat = scipy.io.loadmat(filename)
	rawdata = mat['seatrial_data']

	m = len(rawdata);
	n = len(rawdata[0]);
	#m contains number of rows, n contains the number of columns

	############ Extract Useful data ###################
	actualData = np.zeros((46080,192));
	k=1
	i=1
	for j in range (0,1536):
	    actualData[(j)*30+i-1:(j)*30+i+30-1-1,:]= rawdata[(j)*32+k+32-1:(j)*32+k+32-1-1-1+32-1,:];
	mini = 9999;
	maxi = -9999;

	x = len(actualData);
	y = len(actualData[0]);
	for i in range(x):
	    for j in range(y):
	        if(mini > actualData[i,j]):
	            mini = actualData[i,j]
	        if(maxi < actualData[i,j]):
	            mixi = actualData[i,j]
	divider = max(abs(mini),maxi);
	for i in range(x):
	    for j in range(y):
	        actualData[i,j] = actualData[i,j]/divider;
	#print (actualData)
	########### Normalization Ends #####################

	########### Check if Along Map and across Map data. ######
	summedData=np.zeros((1536,n));
	finalMat = np.zeros((1536,n));
	for i in range(0,n):
	    for t in range(0,1536):
	        for q in range(0,30):
	            summedData[t,i] += (actualData[(t)*30+q,i]);       
	    
	#s = len(summedData[1])
	#print (s)
	print ("good to go")
	for i in range(0,192):
	    #h = abs(hilbert(summedData[:,i]))
	    h = abs((summedData[:,i]))
	    finalMat[:,i] =255 - (abs((((h[:]-min(h[:]))/(max(h[:])-min(h[:])))*255)))

def insertMetalPlate():
	global finalMat
	for i in range(850,950):
	    for j in range(80,120):
	        finalMat[i,j] = random.randint(150,200)

def plot2d():
	global finalMat
	fig = plt.figure(figsize=(6, 10))
	plt.rcParams["figure.figsize"] = 1,90
	ax = fig.add_subplot(111)
	ax.set_title('colorMap')
	plt.imshow(finalMat)
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
	entry_B.insert(END,filename)

def selectFileChirpData():
    global filename2
    filename2=askopenfilename()
    print(filename2)
    entry_C.insert(END,filename2)

def interpolate(arr2):
	global depthsArr
	n = 20;
	depthsArr = np.zeros((n,192))
	for x in range(0,192):
		#if arr2[x]>7:
		depthsArr[0,x]=-1*arr2[x]
		#else:
		#	depthsArr[0,x]=7
	for i in range(1,n):
	    for j in range(0,192):
	        rand = random.randint(-10,11)
	        depthsArr[i,j] = depthsArr[0,j] + (rand/50)

	#print (depthsArr)
	#return depthsArr

def interpolateAndCreateObject(arr2):
	global depthsArr
	n = 20;
	depthsArr = np.zeros((n,192));
	for x in range(0,192):
		#f arr2[x]>7:
		depthsArr[0,x]=-1*arr2[x]
		#else:
		#	depthsArr[0,x]=7
	for i in range(1,n):
	    for j in range(0,192):
	        rand = random.randint(-10,11)
	        depthsArr[i,j] = depthsArr[0,j] + (rand/100)
	for i in range(8,12):
		for j in range(80,120):
			depthsArr[i,j]+=1.5;
	for i in range(9,11):
		for j in range(90,110):
			depthsArr[i,j]+=0.5
	for i in range(10,11):
		for j in range(10,110):
			depthsArr[i,j]+=0.25

def plot3d():
	global depthsArr
	fig=plt.figure()
	ax=fig.gca(projection='3d')
	X=np.arange(0,1920,10)
	#print(X)
	Y=np.arange(0,200,10)
	#print(Y)
	X, Y = np.meshgrid(X, Y)
	Z=depthsArr
	surf=ax.plot_surface(X,Y,Z, cmap=cm.coolwarm, rstride=10,cstride=10,linewidth=0, antialiased=False)
	ax.set_zlim(0, 8)
	ax.zaxis.set_major_locator(LinearLocator(10))
	ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')
	fig.colorbar(surf, shrink=0.5, aspect=10)
	# #axes = Axes3D(fig)
	# canvas=FigureCanvasTkAgg(fig,master=ctr_mid)
	
	# #map = Basemap()

	# #axes.add_collection3d(map.drawcoastlines(linewidth = 0.3, color = "white"))
	# #axes.add_collection3d(map.drawcountries(linewidth = 0.3, color = "white"))
	# #axes.add_collection3d(map.drawstates(linewidth = 0.3, color = "white"))
	# canvas.show()
	# canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=1)
	plt.show()

def plot3dByPlotly():
	global depthsArr
	data = [go.Surface(z=depthsArr)]
	layout = go.Layout(scene = dict(
		xaxis = dict(
			nticks=18, 
			range = [0,192],
			),
		yaxis = dict(
			nticks=20, 
			range = [0,20],
			),
		zaxis = dict(
			nticks=10, 
			range = [-10,10],
			),
		),
	width=1000,
	margin=dict(
		r=20, l=10,b=10, t=10
		)
	)
	fig = go.Figure(data=data,layout=layout)
	py.offline.plot(fig)

def getDepths():
	i=0
	global finalMat
	data2=finalMat
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
				if depths[i]>7.5:
					depths[i]=7.5
				elif depths[i]<6.5:
					depths[i]=6.5
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
	#print(depths)
	return depths

def simple2dPlot():
	generate2DPlot()
	plot2d()

def plot2DwithMetalPlate():
	generate2DPlot()
	insertMetalPlate()
	plot2d()

def simple3dPlot():	
	generate2DPlot()
	interpolate(getDepths())	
	plot3dByPlotly()

def plot3dWithMetalStrip():
	generate2DPlot()
	insertMetalPlate()
	interpolate(getDepths())	
	plot3dByPlotly()

def plot3dWithObject():
	generate2DPlot()
	interpolateAndCreateObject(getDepths())	
	plot3dByPlotly()

########################################################################
root = Tk()
root.title('2D image generation for SONAR data')
root.geometry('{}x{}'.format(400, 500))

# create all of the main containers
top_frame_container = Frame(root, bg='#ddd', width = 200, height=90, pady=5, padx=5)
top_frame = Frame(top_frame_container, bg='white', width = 300, height=50,padx=32,pady=10)
center = Frame(root, bg='#ddd', width=200, height=190, padx=5, pady=5)
#btm_frame = Frame(root, bg='white', width = 450, height = 45, pady=3)
#btm_frame2 = Frame(root, bg='lavender', width = 450, height = 60, pady=3)

# layout all of the main containers
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
top_frame_container.grid(sticky="ew")
top_frame.grid(row=1, sticky="nsew")
center.grid(row=1, sticky="nsew")
#btm_frame.grid(row = 3, sticky="ew")
#btm_frame2.grid(row = 4, sticky="ew")

# create the center widgets
top_frame.grid_rowconfigure(1,weight=1)
top_frame.grid_columnconfigure(1,weight=1)
center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(0, weight=1)

# ctr_left = Frame(center, bg='blue', width=100, height=190)
#ctr_mid = Frame(center, bg='white', width=525, height=190, padx=10, pady=3)
ctr_right = Frame(center, bg='white', width=200, height=190, padx=10, pady=3)

# ctr_left.grid(row=0, column = 0, sticky="ns")
#ctr_mid.grid(row=0, column = 1, sticky="ns")
ctr_right.grid(sticky="nsew")
# create the widgets for the top frame
#model_label = Label(top_frame, text = 'Model Dimensions')
width_label = Label(ctr_right,background='white', text = 'Rows: ',borderwidth = 5)
length_label = Label(ctr_right,background='white', text = 'Columns:')
height_label = Label(ctr_right,background='white', text = 'Start Point:')
button_b1=Button(ctr_right,text="Generate 2D plot",width=25, command=simple2dPlot)
button_b2=Button(top_frame,text="Browse SONAR File",width=16, command=selectFileData)
button_b3=Button(top_frame,text="Browse Chirp File",width=16 , command=selectFileChirpData)
button_b4=Button(ctr_right,text="Generate 2D plot with Metal Strip",width=25 , command=plot2DwithMetalPlate)
button_b5=Button(ctr_right,text="Generate 3D plot",width=25 , command=simple3dPlot)
button_b6=Button(ctr_right,text="Generate 3D plot with Metal Strip",width=25 , command=plot3dWithMetalStrip)
button_b7=Button(ctr_right,text="Generate 3D plot with Object",width=25 , command=plot3dWithObject)
entry_W = Entry(ctr_right, background="white")
entry_L = Entry(ctr_right, background="white")
entry_H = Entry(ctr_right, background="white")
entry_B = Entry(top_frame,width=30 , background="white")
entry_C = Entry(top_frame,width=30 ,background="white")
# use e.get() to get the string.
#use int(e.get())to convert to int
# use button_b1.bind('<BUTTON-1>',functionName)
# layout the widgets in the top frame
#model_label.grid(row = 0, columnspan = 3)

width_label.grid(row = 1, column = 0,padx=10, pady=10)
length_label.grid(row = 2, column = 0,padx=10, pady=10)
height_label.grid(row = 3, column = 0,padx=10, pady=10)
button_b1.grid(row = 4, column=0,padx=10, pady=10)
button_b2.grid(row=0,column=0,padx=10,pady=5)
button_b3.grid(row=1,column=0,padx=10,pady=5)
button_b4.grid(row=5,column=0,padx=10,pady=5)
button_b5.grid(row=6,column=0,padx=10,pady=5)
button_b6.grid(row=7,column=0,padx=10,pady=5)
button_b7.grid(row=8,column=0,padx=10,pady=5)
entry_W.grid(row = 1, column = 1)
entry_L.grid(row = 2, column = 1)
entry_H.grid(row = 3, column = 1)
entry_B.grid(row=0,column=1)
entry_C.grid(row=1,column=1)
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
root.mainloop()
