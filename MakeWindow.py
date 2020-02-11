import sys
import types
import ctypes
import pyqtgraph as pg
import win32api
import win32con
import win32gui
import time
import multiprocessing
import ctypes.wintypes
import numpy as np
import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctypes.wintypes import POINT
from functools import partial

import Menuaction
import timelinetest

class childframe(QWidget):
	def __init__(self,parent=None):
		super(childframe,self).__init__(parent)
		self.parent = parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.initResized = False

	def setChildWidgetInfo(self):
		self.ChildrenWidget = []

		for widget in self.findChildren(QWidget):
			self.ChildrenWidget.append(widget)

		
		self.FrameSize_width = self.size().width()
		self.FrameSize_height = self.size().height()

		self.ChildrenWidget_baseSize = []
		for childwidget in self.ChildrenWidget:
			self.ChildrenWidget_baseSize.append([childwidget.size().width(),childwidget.size().height()])


	def nativeEvent(self,eventType,message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if eventType == "windows_generic_MSG":
			if msg.message == win32con.WM_NCLBUTTONDOWN:
				nHittest = int(msg.wParam)
				if nHittest in [win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
					self.setChildWidgetInfo()

		return False, 0
			
	def resizeEvent(self,e):
		if self.initResized:
			xSizeChangeRatio = (1+(e.size().width() - self.FrameSize_width ) / self.FrameSize_width)
			ySizeChangeRatio = (1+(e.size().height() - self.FrameSize_height )/ self.FrameSize_height)
			i=0
			for childwidget in self.ChildrenWidget:
				childwidget.resize(self.ChildrenWidget_baseSize[i][0]*xSizeChangeRatio, self.ChildrenWidget_baseSize[i][1]*ySizeChangeRatio)
				i=i+1
		else:
			self.setChildWidgetInfo()
			self.initResized = True
	





def mkSignalWindow(self):
	def viewbox_resized(viewbox):
		if not self.parent.Resized:
			viewbox_pos_x = viewbox.geometry().x()
			viewbox_pos_y = viewbox.geometry().y()
			viewbox_height = viewbox.size().height()

			margin = (self.SignalPlot.geometry().height() - viewbox_height)/2
			LabelBox = QVBoxLayout()
			LabelBox.setContentsMargins(10,5+self.SignalPlot.geometry().y()+margin,0,self.geometry().height()-self.SignalPlot.geometry().height()+margin)
			for i in range(self.parent.Ch_num):
				
				lbl = QLabel(self.parent.Selected_Chs[i])
				lbl.setFixedWidth(lbl.sizeHint().width())
				lbl.setScaledContents(True)
				lbl.setStyleSheet('color:yellow; background:#333333')
				if i == 0:
					LabelBox.addStretch((viewbox_height/(self.parent.Ch_num+1))-lbl.sizeHint().height()/2)

				LabelBox.addWidget(lbl)
				if i == self.parent.Ch_num-1:
					LabelBox.addStretch((viewbox_height/(self.parent.Ch_num+1))-lbl.sizeHint().height()/2)
				else:
					LabelBox.addStretch((viewbox_height/(self.parent.Ch_num+1))-lbl.sizeHint().height())
				
			

			self.setLayout(LabelBox)

		


			self.parent.Resized = True

	self.parent.signal_frame_width = self.frameGeometry().width()
	self.parent.signal_frame_height = self.frameGeometry().height()

	pg.setConfigOption('background', '#333333')
	pg.setConfigOption('foreground', 'y')
	self.SignalWindow = pg.GraphicsLayoutWidget(parent=self)
	#
	
	self.SignalWindow.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
	self.SignalWindow.setGeometry(0,0,self.parent.signal_frame_width,self.parent.signal_frame_height)
	

	self.SignalPlot = self.SignalWindow.addPlot(enableMouse=False,row=0,col=0)
	self.SignalPlot.showButtons()

	#self.SignalPlot.setBackground('w')

	self.SignalPlot.setContentsMargins(0, 0, 0, 0)
	
	plotstyle = pg.mkPen(color='y',width=1)
	self.SignalPlot.hideAxis('left')
	self.SignalPlot.hideAxis('bottom')
	self.SignalPlot.setXRange(0,self.parent.TimeScale*(self.parent.Frequency),padding=0)
	self.SignalPlot.setYRange(-100,(self.parent.Ch_num-1)*100+100,padding=0)
	self.SignalPlot.enableAutoRange(axis='xy',enable=False)
	self.SignalPlot.setMouseEnabled(x=True,y=True)
	self.SignalPlot.setDownsampling(True,mode='mean')
	self.SignalPlot.setClipToView(True)

	#self.SignalPlot.addLine(x=line)
#	pg.setConfigOption('wheelspin',False)
	self.parent.plotdic=[]
	self.parent.linedic=[]
	self.parent.PlotData={'x' : [], 'y' : []}
	
	
	for i in range(self.parent.Ch_num):
		self.parent.plotdic.append(self.SignalPlot.plot(pen=plotstyle, name=str(i)))
		self.parent.PlotData['x'].append(list(range(0,3*10*60*self.parent.Frequency)))
		self.parent.PlotData['y'].append(self.parent.EDF.readSignal(self.parent.Selected_Channels_index[i],self.parent.playtime*self.parent.Frequency,3*10*60*self.parent.Frequency)+i*100)
		self.parent.plotdic[i].setData(self.parent.PlotData['x'][i],self.parent.PlotData['y'][i])

	a = self.parent.plotdic[self.parent.Ch_num-1]
		

	self.PlotViewBox = self.SignalPlot.getViewBox()
	self.PlotViewBox.frame = self
	
	self.PlotViewBox.setLimits(xMin=0,yMin=-100,yMax=(self.parent.Ch_num-1)*100+100,
								minYRange = (self.parent.Ch_num-1)*100+200,maxYRange=(self.parent.Ch_num-1)*100+200
								,minXRange=self.parent.Frequency*0.1,maxXRange=self.parent.Frequency*600)
	self.parent.Resized = False


	# Move event trigger
	proxy = QGraphicsProxyWidget()
	button_left = QPushButton()
	icon_left = QIcon('oneleft.png')
	button_left.setIcon(icon_left)

	proxy2 = QGraphicsProxyWidget()
	button_right = QPushButton()
	icon_right = QIcon('oneright.png')
	button_right.setIcon(icon_right)

	proxy3 = QGraphicsProxyWidget()
	button_right_u = QPushButton()
	icon_right_u = QIcon('tworight.png')
	button_right_u.setIcon(icon_right_u)

	proxy4 = QGraphicsProxyWidget()
	button_left_u = QPushButton()
	icon_left_u = QIcon('twoleft.png')
	button_left_u.setIcon(icon_left_u)
	
	proxy.setWidget(button_left_u)
	proxy2.setWidget(button_left)
	proxy3.setWidget(button_right)
	proxy4.setWidget(button_right_u)

	self.TestButton = self.SignalWindow.addLayout(row=1,col=0)
	self.TestButton.setMaximumWidth(120)
	self.TestButton.addItem(proxy)
	self.TestButton.addItem(proxy2)
	self.TestButton.addItem(proxy3)
	self.TestButton.addItem(proxy4)
	
	self.SignalWindow.show()

	
	

	
	"""
	def Manager():
		m = MyManager()
		m.start()
		return m

	plot = self.SignalPlot

	MyManager.register('SignalPlot',plot)

	manager = Manager()
	self.sigPlot_copy = manager.SignalPlot()
	self.pool = multiprocessing.Pool(multiprocessing.cpu_count())
	"""

	def PlayTimeUpdated(self):
		self.parent.DPFrame.win.getPlaytimeChanged(self.parent.playtime)

	# self = button 클래스임
	def viewrange_changed(self):
		self.frame.parent.TimeScale = ((self.viewRange()[0][1]-self.viewRange()[0][0])/self.frame.parent.Frequency)//self.frame.parent.unit/self.frame.parent.Frequency
		self.frame.parent.playtime = (self.viewRange()[0][0]/self.frame.parent.Frequency)//self.frame.parent.unit/self.frame.parent.Frequency





	def move_left(self):
		self.parent.btn_click = True
		self.parent.playtime -= 1
		self.parent.btn_click = False
		

	def move_right(self):
		self.parent.btn_click = True
		self.parent.playtime += 1
		self.parent.btn_click = False
		
	def move_left_u(self):
		self.parent.btn_click = True
		self.parent.playtime -= self.parent.TimeScale
		self.parent.btn_click = False

	def move_right_u(self):
		self.parent.btn_click = True
		self.parent.playtime += self.parent.TimeScale
		self.parent.btn_click = False

		

	
	
	#self.update.start()
	
	

	self.PlayTimeUpdated = partial(PlayTimeUpdated,self)
	self.move_left = partial(move_left,self)
	self.move_right = partial(move_right,self)
	self.move_left_u = partial(move_left_u,self)
	self.move_right_u = partial(move_right_u,self)

	self.PlotViewBox.sigResized.connect(viewbox_resized)
	self.PlotViewBox.sigXRangeChanged.connect(viewrange_changed)
	button_left.clicked.connect(self.move_left)
	button_left_u.clicked.connect(self.move_left_u)
	button_right.clicked.connect(self.move_right)
	button_right_u.clicked.connect(self.move_right_u)




def mkChannelSelect(self):
	
	class ChannelWindow(QMainWindow):
		def __init__(self,parent=None):
			super(ChannelWindow,self).__init__(parent)
			self.Main = parent
			self.initUI()


		def setChannel(self):
			self.Main.ChannelOpen = True
			self.Main.Selected_Chs = []
			channels = self.ListWidget.selectedItems()
			self.Main.Ch_num = len(channels)
			self.Main.Selected_Channels_index = []
			for i in channels:
				for j in range(self.Main.FullCh_num):
					if i.text() == self.Main.EDF.getLabel(j):
						self.Main.Selected_Channels_index.append(j)
						self.Main.Selected_Chs.append(i.text())
						break

			self.Main.SignalFrame = childframe(self.Main)
			self.Main.DPNameFrame = childframe(self.Main)
			self.Main.DPFrame = childframe(self.Main)
			self.Main.SignalFrame.setGeometry(0,20,
											self.Main.geometry().width(),
											self.Main.geometry().height()*0.8-20)
			self.Main.DPNameFrame.setGeometry(0,
											self.Main.geometry().height()*0.8,
											self.Main.geometry().width()*1/25,
											self.Main.geometry().height()*0.2)
			self.Main.DPFrame.setGeometry(self.Main.geometry().width()*1/25,
										self.Main.geometry().height()*0.8,
										self.Main.geometry().width()*24/25,
										self.Main.geometry().height()*0.2)
			mkSignalWindow(self.Main.SignalFrame)
			timelinetest.detPredBar(self.Main.DPFrame)
			timelinetest.dfname(self.Main.DPNameFrame)
			self.Main.SignalFrame.show()
			self.Main.DPFrame.show()
			self.Main.DPNameFrame.show()
			self.close()
			


		def Cancel(self):
			self.Main.ChannelOpen = False
			self.close()
			
		def initUI(self):
			widget = QWidget()
			vbox = QVBoxLayout()
			hbox = QHBoxLayout()
			self.ListWidget = QListWidget()
			self.ListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
			for index in range(self.Main.FullCh_num):
				item = self.ListWidget.addItem(self.Main.EDF.getLabel(index))

			self.ListWidget.selectAll()

			OKButton = QPushButton('OK')
			CancelButton = QPushButton('Cancel')
			OKButton.clicked.connect(self.setChannel)
			CancelButton.clicked.connect(self.Cancel)
			hbox.addWidget(OKButton)
			hbox.addWidget(CancelButton)
			
			vbox.addStretch(1)
			vbox.addWidget(self.ListWidget)
			vbox.addStretch(2)
			vbox.addLayout(hbox)
			widget.setLayout(vbox)
			self.setCentralWidget(widget)
			self.setGeometry(300,300,300,300)
			self.show()
	
	
	self.chWindow = ChannelWindow(self)
	

	
















