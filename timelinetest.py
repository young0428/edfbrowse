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


def makeDataList(self):

	self.lendy = len(self.detData)
	self.lenpy = len(self.predData)
	self.detx = range(self.lendy+1)
	self.predx = range(self.lenpy+1)


def dfname(parent):
	container = QWidget(parent)
	container.setStyleSheet('background:#333333;')
	container.setGeometry(0,0,parent.geometry().width(),parent.geometry().height())

	VLayout = QVBoxLayout()
	VLayout.setContentsMargins(parent.geometry().width()*0.1,0,0,0)
	container.setLayout(VLayout)
	
	#VLayout.setContentsMargins(0,0,0,0)
	
	a = QLabel("Detection")
	a.setStyleSheet('color:white; background:#333333;')
	a.setAlignment(Qt.AlignCenter)

	b = QLabel("Prediction")
	b.setStyleSheet('color:white ; background:#333333;')
	b.setAlignment(Qt.AlignCenter)
	VLayout.addWidget(a)
	VLayout.addWidget(b)
	
	

	


	"""
	win = pg.GraphicsLayoutWidget(parent=parent)
	win.setGeometry(0,0,parent.geometry().width(),parent.geometry().height())

	dettext = pg.TextItem(text="Detection",color=(200,200,200))
	predtext = pg.TextItem(text="Prediction",color=(200,200,200))

	detname = win.addViewBox(1,1)
	detname.addItem(dettext)
	predname = win.addViewBox(2,1)
	predname.addItem(predtext)
	"""
	
def getPlaytimeChanged(self,playtime):
	hour = playtime
	self.parent.DPFrame.detviewbox.timeline.setPos(hour)
	self.parent.DPFrame.predviewbox.timeline.setPos(hour)
	


def detPredBar(parent):
	parent.getPlaytimeChanged = partial(getPlaytimeChanged,parent)

	#window
	#pg.setConfigOption('background','#303030')
	parent.win = pg.GraphicsLayoutWidget(parent=parent)
	parent.win.setGeometry(0,0,parent.geometry().width()+2,parent.geometry().height())
	
	parent.lay = parent.win.addLayout(0,0)
	parent.lay.setBorder()
	
	parent.dettime = pg.AxisItem(orientation='bottom')
	parent.dettime.setScale(1/3600)
	parent.dettime.setTickSpacing(major=1,minor=1/6)
	parent.dettime.setGrid(255)
	parent.dettime.setPen('#A0A0A0')

	parent.predtime = pg.AxisItem(orientation='bottom')
	parent.predtime.setScale(1/3600)
	parent.predtime.setTickSpacing(major=1,minor=1/6)
	parent.predtime.setGrid(255)
	parent.predtime.setPen('#A0A0A0')




	#DetectPlot
	parent.det = parent.lay.addPlot(1,1,axisItems={"bottom":parent.dettime})

	parent.det.showAxis('bottom',show=True)
	parent.det.showAxis('left',show=False)

	parent.det.enableAutoRange(axis='y', enable=False)
	parent.det.setMouseEnabled(x=True,y=False)
	parent.det.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=parent.parent.lendy,yMin=0,yMax=1)
	
	parent.det.p = parent.det.plot(parent.parent.detx,parent.parent.detData,stepMode=True,
	 fillLevel=0,brush=(210,33,26,255),pen=pg.mkPen('#D2211A'))
	
	
	#predictPlot
	parent.pred = parent.lay.addPlot(2,1,axisItems={"bottom":parent.predtime})

	parent.pred.showAxis('bottom',show=True)
	parent.pred.showAxis('left',show=False)

	parent.pred.enableAutoRange(axis='y', enable=False)
	parent.pred.setMouseEnabled(x=True,y=False)
	parent.pred.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=parent.parent.lenpy,yMin=0,yMax=1)
	
	parent.pred.p = parent.pred.plot(parent.parent.predx,parent.parent.predData,stepMode=True, fillLevel=0,
					brush=(32,130,55,255),pen=pg.mkPen('#208237'))
	
	
	#Get Viewbox
	
	parent.detviewbox = parent.det.getViewBox()
	parent.predviewbox = parent.pred.getViewBox()
	parent.detviewbox.frame = parent
	parent.predviewbox.frame = parent

	#Timeline
	dettimeline = pg.InfiniteLine(pen=pg.mkPen('y',width=2),
							   hoverPen=pg.mkPen('y',width=2),
							   movable=True)
	
	parent.detviewbox.timeline = dettimeline
	parent.detviewbox.addItem(dettimeline)

	predtimeline = pg.InfiniteLine(pen=pg.mkPen('y',width=2),
							   hoverPen=pg.mkPen('y',width=2),
							   movable=True)
	
	parent.predviewbox.timeline = predtimeline
	parent.detviewbox.addItem(predtimeline)
	
	
	#InfLabel
	pg.InfLineLabel(dettimeline)
	pg.InfLineLabel(predtimeline)
	parent.det.addItem(dettimeline)
	parent.pred.addItem(predtimeline)



	def mouseClickEvent(self,e):
		fre = self.frame.parent.Frequency
		clktime = self.mapSceneToView(e.scenePos()).x()
		self.timeline.setPos(clktime)
		
		self.frame.parent.playtime = clktime//(1/fre)*(1/fre)
		
	def MoveFinished(self,obj):
		self.frame.parent.playtime = (obj.getXPos()//self.frame.parent.unit)/self.frame.parent.Frequency

	parent.detviewbox.mouseClickEvent = partial(mouseClickEvent,parent.detviewbox)	
	parent.predviewbox.mouseClickEvent = partial(mouseClickEvent,parent.predviewbox)
	parent.detviewbox.MoveFinished = partial(MoveFinished,parent.detviewbox)
	parent.predviewbox.MoveFinished = partial(MoveFinished,parent.predviewbox)

	predtimeline.sigPositionChangeFinished.connect(parent.predviewbox.MoveFinished)
	dettimeline.sigPositionChangeFinished.connect(parent.detviewbox.MoveFinished)