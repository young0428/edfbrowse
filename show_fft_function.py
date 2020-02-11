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


signal_name = 'plz'

start_xpx = 0
start_ypx = 0
xpx = 1600
ypx = 250
in_xpx = xpx - 2*start_xpx
in_ypx = ypx - 2*start_ypx


def getplaytimechanged(self):
	data = make_data(self,self.EDF)
	self.plt1.clearPlots()
	self.maxpsd = max(data.psd)
	self.plt1.setYRange(0,self.maxpsd)
	self.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+self.maxpsd)
	self.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))

def gettimescalechanged(self):
	data = make_data(self,self.EDF)
	self.plt1.clearPlots()
	self.maxpsd = max(data.psd)
	self.plt1.setYRange(0,self.maxpsd)
	self.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+self.maxpsd)
	self.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))

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
	
	parent.win.setGeometry(start_xpx,start_ypx,in_xpx,in_ypx)
	#parent.win.setWindowFlags(Qt.FramelessWindowHint)
	
	parent.ffttimeleft = pg.AxisItem(orientation='left')
	parent.ffttimeleft.setGrid(255)
	parent.ffttimeleft.setPen('#A0A0A0')

	parent.ffttime = pg.AxisItem(orientation='bottom')
	parent.ffttime.setGrid(255)
	parent.ffttime.setPen('#A0A0A0')

	parent.plt1 = parent.win.addPlot(axisItems={'left':parent.ffttimeleft,'bottom':parent.ffttime})
	parent.plt1.showGrid(x=True, y=True,alpha=1)
	parent.plt1.setLabel('bottom', text='Frequency', units='Hz')
	parent.plt1.setLabel('left', text='PSD', units='uV^2/Hz')
	parent.plt1.enableAutoRange(axis='xy', enable=False)
	parent.plt1.setYRange(0,parent.maxpsd)
	parent.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+parent.maxpsd)
	parent.plt1.setMouseEnabled(x=False,y=False)
	parent.plt1.plot(data.bins,data.psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))

class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		self.MainSize_x = xpx
		self.MainSize_y = ypx
		self.WindowChildren = []
		self.initUI()

	def initUI(self):
		show_fft(self,make_data)

		self.resize(xpx,ypx)
		self.show()

	def nativeEvent(self,eventType,message):
			msg = ctypes.wintypes.MSG.from_address(message.__int__())
			if eventType == "windows_generic_MSG":
				if msg.message == win32con.WM_NCLBUTTONDOWN:
					nHittest = int(msg.wParam)
					if nHittest in [win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
						self.WindowChildren = []

						for child in self.findChildren(QWidget):
							if 'graphics' in str(child).lower():
								self.WindowChildren.append(child)
						
						if not nHittest == win32con.HTCAPTION:
							
							self.MainSize_x = self.size().width()
							self.MainSize_y = self.size().height()
							

						self.WindowChildren_baseSize = []
						for WindowChild in self.WindowChildren:
							self.WindowChildren_baseSize.append([WindowChild.size().width(),WindowChild.size().height()])
						

			return False, 0

	def resizeEvent(self,e):
		xSizeChangeRatio = (1+(e.size().width() - self.MainSize_x ) / self.MainSize_x)
		ySizeChangeRatio = (1+(e.size().height() - self.MainSize_y )/ self.MainSize_y)
		i=0
		for WindowChild in self.WindowChildren:
			WindowChild.resize(self.WindowChildren_baseSize[i][0]*xSizeChangeRatio, self.WindowChildren_baseSize[i][1]*ySizeChangeRatio)
			i=i+1

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MyApp()
	sys.exit(app.exec_())
