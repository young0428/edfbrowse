"""
Get from outside
- EDF.class
- playtime
- timescale
- signal number

Event Driven variation
- playtime
- timescale


"""

import pyedflib
from read_edf_function import get_signal_data
import sys
import ctypes
import MakeWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import win32con
import ctypes.wintypes
import numpy as np


class RFbutton(QPushButton):
	def __init__ (self,parent):
		super(RFbutton,self).__init__(parent)
		self.frame = parent
		self.initUI()
		self.frame.button_change = 0  # fixed = 0 , relative = 1
		self.clicked.connect(self.btn_clicked)


	def initUI(self):
		self.setText("F")
		self.setGeometry(5,5,25,25)
		self.setMinimumWidth(20)
		self.setMinimumHeight(20)
		self.setMaximumWidth(25)
		self.setMaximumHeight(25)


	def btn_clicked(self):
		if self.frame.button_change == 0:
			self.frame.button_change = 1
			self.setText("R")

			data = make_data(self.frame.parent,self.frame.parent.EDF)
			maxpsd = max(data.psd)
			self.frame.plt1.setYRange(0,maxpsd)
			self.frame.plt1.setLimits(minXRange=50,maxXRange=50,xMin=0,xMax=100,yMin=0)
		else:
			self.frame.button_change = 0
			self.setText("F")

			maxpsd = self.frame.maxpsd
			self.frame.plt1.setYRange(0,maxpsd)
			self.frame.plt1.setLimits(minXRange=50,maxXRange=50,xMin=0,xMax=100,yMin=0)


class scalebutton(QPushButton):
	def __init__ (self,parent):
		super(scalebutton,self).__init__(parent)
		self.frame = parent	
		self.initUI()
		self.clicked.connect(self.showDialog)

	def initUI(self):
		self.setText("Max PSD")
		self.setGeometry(5,self.frame.frameGeometry().height()-30,120,25)
		self.setMinimumWidth(110)
		self.setMaximumWidth(120)
		self.setMinimumHeight(20)
		self.setMaximumHeight(25)

	def showDialog(self):
		setpsd, ok = QInputDialog.getDouble(self, 'Set Scale','Current Scale: '+str(self.frame.maxpsd))

		if ok:
			self.frame.maxpsd = setpsd
			self.frame.plt1.setYRange(0,setpsd)



def getplaytimechanged(self):
	data = make_data(self,self.EDF)

	if self.FFTFrame.button_change == 1:
		maxpsd = max(data.psd)
		self.FFTFrame.plt1.setYRange(0,maxpsd)
		self.FFTFrame.plt1.setLimits(minXRange=50,maxXRange=50,xMin=0,xMax=100,yMin=0)
	self.FFTFrame.plt1.p.setData(data.bins,data.psd)

def gettimescalechanged(self):
	data = make_data(self,self.EDF)
	
	if self.FFTFrame.button_change == 1:
		maxpsd = max(data.psd)
		self.FFTFrame.plt1.setYRange(0,maxpsd)
		self.FFTFrame.plt1.setLimits(minXRange=50,maxXRange=50,xMin=0,xMax=100,yMin=0)
	self.FFTFrame.plt1.p.setData(data.bins,data.psd)

class make_data:
	def __init__(self,main,EDF):
		self.playtime = main.playtime
		self.timescale = main.TimeScale
		self.signum = main.signum


		instant_list = [self.signum]
		prefft = get_signal_data(EDF, self.playtime, self.timescale, instant_list)
		del instant_list

		#realnumber fft
		fft = np.fft.rfft(prefft[0])
		samplefreq = EDF.getSampleFrequency(self.signum)
		n = len(fft)
		absfft = abs(fft)/(n-1)

		self.psd = 2*absfft*absfft
		self.bins = np.linspace(0,samplefreq//2,n+1)



def show_fft(parent,data):

	parent.maxpsd = 70	#max(data.psd)
	
	parent.win = pg.GraphicsLayoutWidget(parent=parent)
	parent.win.setGeometry(0,0,parent.geometry().width(),parent.geometry().height())
	
	parent.ffttimeleft = pg.AxisItem(orientation='left')
	parent.ffttimeleft.setGrid(255)
	parent.ffttimeleft.setPen('#A0A0A0')

	parent.ffttime = pg.AxisItem(orientation='bottom')
	parent.ffttime.setGrid(255)
	parent.ffttime.setTickSpacing(major=10,minor=1)
	
	parent.ffttime.setPen('#A0A0A0')

	parent.plt1 = parent.win.addPlot(axisItems={'left':parent.ffttimeleft,'bottom':parent.ffttime})
	parent.plt1.getViewBox().frame = parent

	parent.plt1.showGrid(x=True, y=True,alpha=1)
	parent.plt1.setLabel('bottom', text='Frequency', units='Hz')
	parent.plt1.setLabel('left', text='PSD', units='uV^2/Hz')
	parent.plt1.enableAutoRange(axis='xy', enable=False)
	parent.plt1.setYRange(0,parent.maxpsd)
	parent.plt1.setLimits(minXRange=50,maxXRange=50,xMin=0,xMax=100,yMin=0)
	parent.plt1.setMouseEnabled(x=False,y=False)
	parent.plt1.p = parent.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen(color='g',width=0.6))


	btn = RFbutton(parent)
	btn2 = scalebutton(parent)