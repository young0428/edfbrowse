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
	win = pg.GraphicsLayoutWidget(parent=parent)
	win.setGeometry(0,0,parent.geometry().width(),parent.geometry().height())
	"""
	dettext = pg.TextItem(text="Detection",color=(200,200,200))
	predtext = pg.TextItem(text="Prediction",color=(200,200,200))
	
	detname = addPlot(1,1)
	detname.addItem(dettext)
	predname = addPlot(2,1)
	predname.addItem(predtext)
	"""
def getPlaytimeChanged(self,playtime):
	hour = playtime / 3600
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
	

	#DetectPlot
	parent.det = parent.lay.addPlot(1,1)
	
	parent.det.showAxis('bottom',show=True)
	parent.det.showAxis('left',show=False)

	parent.det.enableAutoRange(axis='y', enable=False)
	parent.det.setMouseEnabled(x=True,y=False)
	parent.det.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=parent.parent.lendy,yMin=0,yMax=1)
	parent.det.plot(parent.parent.detx,parent.parent.detData,stepMode=True, fillLevel=0,
					brush=(255,0,0,255),pen=pg.mkPen('r'))


	#predictPlot
	parent.pred = parent.lay.addPlot(2,1)

	parent.pred.showAxis('bottom',show=True)
	parent.pred.showAxis('left',show=False)

	parent.pred.enableAutoRange(axis='y', enable=False)
	parent.pred.setMouseEnabled(x=True,y=False)
	parent.pred.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=parent.parent.lenpy,yMin=0,yMax=1)
	parent.pred.plot(parent.parent.predx,parent.parent.predData,stepMode=True, fillLevel=0,
					brush=(0,150,0,255),pen=pg.mkPen((0,150,0,255)))

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

	predtimeline = pg.InfiniteLine(pen=pg.mkPen('y',width=2),
							   hoverPen=pg.mkPen('y',width=2),
							   movable=True)
	parent.predviewbox.timeline = predtimeline

	
	#Detectbar
	parent.dettime = pg.AxisItem(orientation='bottom')
	parent.dettime.setScale(1/3600)
	parent.dettime.setTickSpacing(major=1,minor=1)
	parent.dettime.setGrid(255)
	parent.dettime.setPen('#A0A0A0')
	parent.detviewbox.addItem(parent.dettime)

	'''
	parent.secdet = parent.lay.addViewBox(1,1)
	parent.secdet.showAxis('bottom',show=True)
	parent.secdet.showAxis('left',show=False)
	parent.minordettime = pg.AxisItem(orientation='bottom')
	parent.minordettime.setScale(1%60)
	parent.minordettime.setTickSpacing(major=None,minor=1)
	parent.minordettime.setGrid(255)
	parent.minordettime.setPen('#A0A0A0')
	parent.secdet.addItem(parent.minordettime)
	'''
	#Predictbar
	parent.predtime = pg.AxisItem(orientation='bottom')
	parent.predtime.setScale(1/60)
	parent.predtime.setTickSpacing(major=1/6,minor=1/6)
	parent.predtime.setGrid(255)
	parent.predtime.setPen('#A0A0A0')
	parent.predviewbox.addItem(parent.predtime)

	'''
	parent.secpred = parent.lay.addViewBox(1,1)
	parent.secpred.showAxis('bottom',show=True)
	parent.secpred.showAxis('left',show=False)
	parent.minorpredtime = pg.AxisItem(orientation='bottom')
	parent.minorpredtime.setScale(1%60)
	parent.minorpredtime.setTickSpacing(major=None,minor=1)
	parent.minorpredtime.setGrid(255)
	parent.minorpredtime.setPen('#A0A0A0')
	parent.secpred.addItem(parent.minorpredtime)	
	'''
	#InfLabel
	pg.InfLineLabel(dettimeline)
	pg.InfLineLabel(predtimeline)
	parent.det.addItem(dettimeline)
	parent.pred.addItem(predtimeline)



	def mouseClickEvent(self,e):
		fre = self.parent.parent.Frequency
		clktime = self.mapSceneToView(e.scenePos()).x()
		self.timeline.setPos(clktime)
		
		self.parent.parent.playtime = clktime//(1/fre)*(1/fre)

	parent.detviewbox.mouseClickEvent = partial(mouseClickEvent,parent.detviewbox)	
	parent.predviewbox.mouseClickEvent = partial(mouseClickEvent,parent.predviewbox)