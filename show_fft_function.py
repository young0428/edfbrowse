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

def getplaytimechanged(self):
	data = make_data(self,self.EDF)
	self.FFTFrame.plt1.clearPlots()
	self.FFTFrame.plt1.setYRange(0,self.FFTFrame.maxpsd)
	self.FFTFrame.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+self.FFTFrame.maxpsd)
	self.FFTFrame.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))

def gettimescalechanged(self):
	data = make_data(self,self.EDF)
	self.FFTFrame.plt1.clearPlots()
	self.FFTFrame.plt1.setYRange(0,self.FFTFrame.maxpsd)
	self.FFTFrame.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+self.FFTFrame.maxpsd)
	self.FFTFrame.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))


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
	parent.maxpsd = max(data.psd)
	
	parent.win = pg.GraphicsLayoutWidget(parent=parent)
	parent.win.setGeometry(0,0,parent.geometry().width(),parent.geometry().height())
	
	parent.ffttimeleft = pg.AxisItem(orientation='left')
	parent.ffttimeleft.setGrid(255)
	parent.ffttimeleft.setPen('#A0A0A0')

	parent.ffttime = pg.AxisItem(orientation='bottom')
	parent.ffttime.setGrid(255)
	parent.ffttime.setPen('#A0A0A0')

	parent.plt1 = parent.win.addPlot(axisItems={'left':parent.ffttimeleft,'bottom':parent.ffttime})
	parent.plt1.getViewBox().frame = parent
	
	parent.plt1.showGrid(x=True, y=True,alpha=1)
	parent.plt1.setLabel('bottom', text='Frequency', units='Hz')
	parent.plt1.setLabel('left', text='PSD', units='uV^2/Hz')
	parent.plt1.enableAutoRange(axis='xy', enable=False)
	parent.plt1.setYRange(0,parent.maxpsd)
	parent.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+parent.maxpsd)
	parent.plt1.setMouseEnabled(x=False,y=False)
	parent.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))
