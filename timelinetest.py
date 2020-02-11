import sys
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import win32con
import ctypes.wintypes
import numpy as np
from functools import partial

playtime = 6000
timescale = 10
signum = 6

start_xpx = 0
start_ypx = 0
xpx = 1900
ypx = 200
in_xpx = xpx - 2*start_xpx
in_ypx = ypx - 2*start_ypx


rand_list=[0,0]
for i in range(2):
	a = []
	a = [0]*700+[1]*20
	np.random.shuffle(a)
	rand_list[i] = a

dety = rand_list[0]
predy = rand_list[1]

lendy = len(dety)
lenpy = len(predy)
detx = range(lendy+1)
predx = range(lenpy+1)


def dfname(parent):
	parent.win = pg.GraphicsLayoutWidget(parent=parent)
	parent.win.setGeometry(start_xpx,start_ypx,parent.geometry().width(),parent.geometry().height())


def getPlaytimeChanged(self,playtime):
	hour = playtime/60
	self.detviewbox.timeline.setPos(hour)
	self.predviewbox.timeline.setPos(hour)
	


def detPredBar(parent):
	#window
	pg.setConfigOption('background','#303030')

	parent.win = pg.GraphicsLayoutWidget(parent=parent)
	parent.win.getPlaytimeChanged = partial(getPlaytimeChanged,parent.win)

	parent.win.setGeometry(start_xpx,start_ypx,parent.geometry().width(),parent.geometry().height())
	
	parent.lay = parent.win.addLayout(0,0)
	parent.lay.setBorder()

	#DetPlot
	parent.dettime = pg.AxisItem(orientation='bottom')
	parent.dettime.setScale(1/60)
	parent.dettime.setTickSpacing(major=1,minor=1/6)
	parent.dettime.setGrid(255)
	parent.dettime.setPen('#A0A0A0')

	parent.det = parent.lay.addPlot(1,1,axisItems={'bottom':parent.dettime})

	parent.det.showAxis('bottom',show=True)
	parent.det.showAxis('left',show=False)

	parent.det.enableAutoRange(axis='y', enable=False)
	parent.det.setMouseEnabled(x=True,y=False)
	parent.det.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=lendy,yMin=0,yMax=1)
	parent.det.plot(detx,dety,stepMode=True, fillLevel=0,
					brush=(255,0,0,255),pen=pg.mkPen('r'))

	#predictbar
	parent.predtime = pg.AxisItem(orientation='bottom')
	parent.predtime.setScale(1/60)
	parent.predtime.setTickSpacing(major=1,minor=1/6)
	parent.predtime.setGrid(255)
	parent.predtime.setPen('#A0A0A0')

	#predPlot
	parent.pred = parent.lay.addPlot(2,1,axisItems={'bottom':parent.predtime})

	parent.pred.showAxis('bottom',show=True)
	parent.pred.showAxis('left',show=False)

	parent.pred.enableAutoRange(axis='y', enable=False)
	parent.pred.setMouseEnabled(x=True,y=False)
	parent.pred.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=lenpy,yMin=0,yMax=1)
	parent.pred.plot(predx,predy,stepMode=True, fillLevel=0,
					brush=(0,150,0,255),pen=pg.mkPen((0,150,0,255)))

	timeline1 = pg.InfiniteLine(pen=pg.mkPen('y',width=2),
							   hoverPen=pg.mkPen('y',width=2),
							   pos=playtime/60,
							   movable=True)

	timeline2 = pg.InfiniteLine(pen=pg.mkPen('y',width=2),
							   hoverPen=pg.mkPen('y',width=2),
							   pos=playtime/60,
							   movable=True)

	pg.InfLineLabel(timeline1)
	pg.InfLineLabel(timeline2)
	parent.det.addItem(timeline1)
	parent.pred.addItem(timeline2)

	detviewbox = parent.det.getViewBox()
	parent.win.detviewbox = detviewbox
	parent.win.detviewbox.parent = parent
	detviewbox.timeline = timeline1
	predviewbox = parent.pred.getViewBox()
	parent.win.predviewbox = predviewbox
	parent.win.predviewbox.parent = parent
	predviewbox.timeline = timeline2



	def mouseClickEvent(self,e):
		fre = self.parent.parent.Frequency
		clktime = self.mapSceneToView(e.scenePos()).x()
		print(clktime)
		self.timeline.setPos(clktime)
		
		self.parent.parent.playtime = clktime*60//(1/fre)*(1/fre)

	detviewbox.mouseClickEvent = partial(mouseClickEvent,parent.win.detviewbox)	
	predviewbox.mouseClickEvent = partial(mouseClickEvent,parent.win.predviewbox)

class MyApp(QWidget):

	def __init__(self):
		super().__init__()
		self.MainSize_x = xpx
		self.MainSize_y = ypx
		self.WindowChildren = []
		self.initUI()

	def initUI(self):
		detPredBar(self)
		self.win.show()
		self.show()
	"""
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
	"""



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = MyApp()
	sys.exit(app.exec_())
