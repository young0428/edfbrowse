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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import win32con
import ctypes.wintypes
import numpy as np

file_name = "C:/Users/dabin/Desktop/EDF/BrainnoEDFfile/brainno05_Fch/Brainno05_1020.edf"

EDF = pyedflib.EdfReader(file_name)
playtime = 30
timescale = 10
signum = 6

signal_name = EDF.getLabel(signum)

start_xpx = 0
start_ypx = 0
xpx = 1900
ypx = 310
in_xpx = xpx - 2*start_xpx
in_ypx = ypx - 2*start_ypx

def show_fft(parent):

	#signal 원본 데이터
	def make_data(EDF, playtime, timescale, signum):
		instant_list = [signum]
		prefft = get_signal_data(EDF, playtime, timescale, instant_list)
		del instant_list

		#realnumber fft
		fft = np.fft.rfft(prefft[0])
		samplefreq = EDF.getSampleFrequency(signum)
		n = len(fft)
		absfft = abs(fft)/(n-1)
		psd = 2*absfft*absfft
		bins = np.linspace(0,samplefreq//2,n+1)

		return bins,psd

	bins,psd = make_data(EDF,playtime,timescale,signum)
	maxpsd = max(psd)

	parent.win = pg.GraphicsLayoutWidget(parent=parent)
	parent.win.setGeometry(start_xpx,start_ypx,in_xpx,in_ypx)
	#parent.win.setWindowFlags(Qt.FramelessWindowHint)
	parent.plt1 = parent.win.addPlot()
	parent.plt1.showGrid(x=True, y=True,alpha=1)
	
	parent.plt1.setLabel('bottom', text='Frequency', units='Hz')
	parent.plt1.setLabel('left', text='PSD', units='uV^2/Hz')
	parent.plt1.enableAutoRange(axis='xy', enable=False)
	parent.plt1.setYRange(0,maxpsd)
	parent.plt1.setLimits(minXRange=100,xMin=0,xMax=100,yMin=0,yMax=5+maxpsd)
	parent.plt1.setMouseEnabled(x=False,y=False)
	parent.plt1.plot(bins,psd,stepMode=True, fillLevel=0, brush=(0,0,0,150),pen=pg.mkPen('g'))

class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		self.MainSize_x = xpx
		self.MainSize_y = ypx
		self.WindowChildren = []
		self.initUI()

	def initUI(self):
		show_fft(self)

		self.setWindowTitle(signal_name)
		self.resize(xpx,ypx)
		self.win.show()
		self.show()

	def nativeEvent(self,eventType,message):
			msg = ctypes.wintypes.MSG.from_address(message.__int__())
			if eventType == "windows_generic_MSG":
				if msg.message == win32con.WM_NCLBUTTONDOWN:
					nHittest = int(msg.wParam)
					if nHittest in [win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
						self.WindowChildren = []


						print(self.findChildren(QWidget))
						for child in self.findChildren(QWidget):
							if 'graphics' in str(child).lower():
								print(child)
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
