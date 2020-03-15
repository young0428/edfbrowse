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
<<<<<<< HEAD
	container = QWidget(parent)
	container.setStyleSheet('background:#333333;')
	container.setGeometry(0,0,parent.geometry().width(),parent.geometry().height())

	VLayout = QVBoxLayout()
<<<<<<< Updated upstream
	VLayout.setContentsMargins(parent.geometry().width()*0.3,0,0,0)
=======
	VLayout.setContentsMargins(parent.geometry().width()*0.1,0,0,0)
	VLayout.setAlignment(Qt.AlignHCenter)
>>>>>>> Stashed changes
	container.setLayout(VLayout)

	#VLayout.setContentsMargins(0,0,0,0)
	
	a = QLabel("Detection")
	a.setStyleSheet('color:white; background:#333333;')
	a.setAlignment(Qt.AlignCenter)
<<<<<<< Updated upstream
	b = QLabel("Prediction")
=======

	b = QLabel("Predict")
	b.setFixedWidth(b.sizeHint().width())
>>>>>>> Stashed changes
	b.setStyleSheet('color:white ; background:#333333;')
	b.setAlignment(Qt.AlignCenter)

	VLayout.addWidget(a)
	VLayout.addWidget(b)
	
	

	


	"""
=======
>>>>>>> parent of f499a00... Merge branch 'design' into Thisss
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
	
<<<<<<< HEAD
<<<<<<< Updated upstream
	parent.dettime = pg.AxisItem(orientation='bottom')
	parent.dettime.setScale(1/3600)
	parent.dettime.setTickSpacing(major=1,minor=1/6)
	parent.dettime.setGrid(255)
	parent.dettime.setPen('#A0A0A0')

	parent.predtime = pg.AxisItem(orientation='bottom')
	parent.predtime.setScale(1/3600)
	parent.predtime.setTickSpacing(major=1,minor=1/6)
	parent.predtime.setGrid(255)
=======
	main = parent.parent

	#tick making
	tick = []
	bigtick = []
	smalltick = []
	for i in range(1,main.lendy):
		if i%60 == 0:
			smalltick.append((int(i),str(i%60)))
			if i%300 == 0:
				if i%3600 == 0:
					bigtick.append((int(i),str(int(i/3600))))
				else:
					smalltick.append((int(i),str(int(i/3600))+':'+str(int((i%3600)//60))))
				
	tick.append(bigtick)
	tick.append(smalltick)

	parent.dettime = pg.AxisItem(orientation='bottom')
	parent.dettime.setTicks(tick)
	parent.dettime.setGrid(100)
	parent.dettime.setPen('#A0A0A0')

	parent.predtime = pg.AxisItem(orientation='bottom')
	parent.predtime.setTicks(tick)
	parent.predtime.setGrid(100)
>>>>>>> Stashed changes
	parent.predtime.setPen('#A0A0A0')




	#DetectPlot
	parent.det = parent.lay.addPlot(1,1,axisItems={"bottom":parent.dettime,"bottom":parent.predtime})
	parent.det.hideButtons()
	parent.det.setClipToView(True)
=======

	#DetectPlot
	parent.det = parent.lay.addPlot(1,1)
	
>>>>>>> parent of f499a00... Merge branch 'design' into Thisss
	parent.det.showAxis('bottom',show=True)
	parent.det.showAxis('left',show=True)

	parent.det.enableAutoRange(axis='y', enable=False)
	parent.det.setMouseEnabled(x=True,y=False)
<<<<<<< Updated upstream
	parent.det.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=parent.parent.lendy,yMin=0,yMax=1)
	parent.det.plot(parent.parent.detx,parent.parent.detData,stepMode=True, fillLevel=0,
					brush=(255,0,0,255),pen=pg.mkPen('r'))


=======
	parent.det.setLimits(minXRange=3600,xMin=0,xMax=parent.parent.lendy,yMin=-1,yMax=1)
	parent.det.setYRange(-1, 1, padding=None, update=False)

	parent.det.p = parent.det.plot(parent.parent.detx,parent.parent.detData,stepMode=True,
	 fillLevel=0,brush=(210,33,26,100),pen=pg.mkPen(color=(210,33,26,100)))



	
	
>>>>>>> Stashed changes
	#predictPlot
<<<<<<< HEAD
	parent.pred = parent.det
	"""
	parent.pred = parent.lay.addPlot(2,1,axisItems={"bottom":parent.predtime})
	
=======
	parent.pred = parent.lay.addPlot(2,1)

>>>>>>> parent of f499a00... Merge branch 'design' into Thisss
	parent.pred.showAxis('bottom',show=True)
	parent.pred.showAxis('left',show=False)

	parent.pred.enableAutoRange(axis='y', enable=False)
	parent.pred.setMouseEnabled(x=True,y=False)
<<<<<<< Updated upstream
	parent.pred.setLimits(minXRange=30,minYRange=1,xMin=0,xMax=parent.parent.lenpy,yMin=0,yMax=1)
	parent.pred.plot(parent.parent.predx,parent.parent.predData,stepMode=True, fillLevel=0,
					brush=(0,150,0,255),pen=pg.mkPen((0,150,0,255)))

=======
	parent.pred.setLimits(minXRange=3600,minYRange=1,xMin=0,xMax=parent.parent.lenpy,yMin=0,yMax=1)
	"""
	parent.pred.pr = parent.det.plot(parent.parent.predx,parent.parent.predData,stepMode=True, fillLevel=0,
					brush=(32,130,55,100),pen=pg.mkPen(color=(32,130,55,100)))

	
	
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
	pg.InfLineLabel(dettimeline)
	pg.InfLineLabel(predtimeline)
=======
	dl = pg.InfLineLabel(dettimeline)
	pl = pg.InfLineLabel(predtimeline)
	dl.setPosition(0.75)
	pl.setPosition(0.25)
>>>>>>> Stashed changes
	parent.det.addItem(dettimeline)
	parent.pred.addItem(predtimeline)



	def mouseClickEvent(self,e):
		fre = self.parent.parent.Frequency
		clktime = self.mapSceneToView(e.scenePos()).x()
		self.timeline.setPos(clktime)
		
<<<<<<< HEAD
<<<<<<< Updated upstream
		self.frame.parent.playtime = clktime//(1/fre)*(1/fre)
=======
		self.frame.parent.playtime = clktime//unit*unit
	
	def wheelEvent(self, ev, axis=None):
		if self.CtrlPress:
			mask = np.array(self.state['mouseEnabled'], dtype=np.float)
			if axis is not None and axis >= 0 and axis < len(mask):
				mv = mask[axis]
				mask[:] = 0
				mask[axis] = mv
			s = ((mask * 0.02) + 1) ** (ev.delta() * self.state['wheelScaleFactor']) # actual scaling factor
			
			center = Point(fn.invertQTransform(self.childGroup.transform()).map(ev.pos()))
			
			self._resetTarget()
			self.scaleBy(s, center)
			self.sigRangeChangedManually.emit(self.state['mouseEnabled'])
			ev.accept()
		else:
			dp_timescale = (self.viewRange()[0][1] - self.viewRange()[0][0])
			movetime = dp_timescale*0.03
			if ev.delta() > 0:
				movetime = movetime * -1


			self.setXRange(self.viewRange()[0][0] + movetime,self.viewRange()[0][1] + movetime,update = True,padding = 0)

	



>>>>>>> Stashed changes
	def MoveFinished(self,obj):
		self.frame.parent.playtime = (obj.getXPos()//self.frame.parent.unit)/self.frame.parent.Frequency
=======
		self.parent.parent.playtime = clktime//(1/fre)*(1/fre)
>>>>>>> parent of f499a00... Merge branch 'design' into Thisss

	parent.detviewbox.mouseClickEvent = partial(mouseClickEvent,parent.detviewbox)	
	parent.predviewbox.mouseClickEvent = partial(mouseClickEvent,parent.predviewbox)
	parent.detviewbox.MoveFinished = partial(MoveFinished,parent.detviewbox)
	parent.predviewbox.MoveFinished = partial(MoveFinished,parent.predviewbox)

	predtimeline.sigPositionChangeFinished.connect(parent.predviewbox.MoveFinished)
	dettimeline.sigPositionChangeFinished.connect(parent.detviewbox.MoveFinished)