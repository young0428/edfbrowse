import sys
import types
import ctypes
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import win32api
import win32con
import win32gui
import time
from ctypes.wintypes import POINT
import ctypes.wintypes
import numpy as np
from functools import partial
import math

import Menuaction


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

					print('Clicked!!')
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
	#self.SignalPlot.hideAxis('left')
	#self.SignalPlot.hideAxis('bottom')
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
		

	self.PlotViewBox = self.SignalPlot.getViewBox()
	self.PlotViewBox.frame = self
	
	self.PlotViewBox.setLimits(xMin=0,yMin=-100,yMax=(self.parent.Ch_num-1)*100+100,
								minYRange = (self.parent.Ch_num-1)*100+200,maxYRange=(self.parent.Ch_num-1)*100+200
								,minXRange=self.parent.Frequency*0.1,maxXRange=self.parent.Frequency*600)
	self.parent.Resized = False
	#print(self.SignalWindow.size().width())

	proxy = QGraphicsProxyWidget()
	button_left = QPushButton()
	icon_left = QIcon('exit.png')
	button_left.setIcon(icon_left)
	
	proxy2 = QGraphicsProxyWidget()
	button_right = QPushButton()
	icon_right = QIcon('exit.png')
	button_right.setIcon(icon_right)

	proxy3 = QGraphicsProxyWidget()
	button_right_u = QPushButton()
	icon_right_u = QIcon('exit.png')
	button_right_u.setIcon(icon_right_u)

	proxy4 = QGraphicsProxyWidget()
	button_left_u = QPushButton()
	icon_left_u = QIcon('exit.png')
	button_left_u.setIcon(icon_left_u)
	
	proxy.setWidget(button_left_u)
	proxy2.setWidget(button_left)
	proxy3.setWidget(button_right)
	proxy4.setWidget(button_right_u)

	




	self.TestButton = self.SignalWindow.addLayout(row=1,col=0)
	self.TestButton.setMaximumWidth(300)
	self.TestButton.addItem(proxy)
	self.TestButton.addItem(proxy2)
	self.TestButton.addItem(proxy3)
	self.TestButton.addItem(proxy4)
	
	


	self.SignalWindow.show()

	



	#     self.parent.PlotData={'x' = [], 'y' = []}
	"""
	class RemoveThread(QThread):
		def __init__(self,parent=None):
			super(RemoveThread,self).__init__(parent)
			self.frame = parent
			self.offset_per_duration = int(self.frame.parent.Frequency * self.frame.parent.duration)
		def __del__(self):
			self.quit()
			self.deleteLayer()
		def run(self):
			#while self.frame.parent.remove:
			preload_duration_num = math.ceil(self.frame.parent.TimeScale*0.5/self.frame.parent.duration)
			start = int(self.frame.parent.playtime/self.frame.parent.duration) - preload_duration_num
			end = math.ceil((self.frame.parent.playtime+self.frame.parent.TimeScale)/(self.frame.parent.duration)) + preload_duration_num
			for i in range(len(self.frame.parent.ck_load)):
				if (start > i or end < i) and self.frame.parent.ck_load[i]==1:
					print('removed!!')
					for ch in range(self.frame.parent.Ch_num):
						self.frame.SignalPlot.removeItem(self.frame.parent.plots[i][ch])

					self.frame.parent.ck_load[i] = 0
			#	self.frame.parent.remove = False



	class PreloadThread(QThread):
		def __init__(self,parent=None):
			super(PreloadThread,self).__init__(parent)
			self.frame = parent
			self.offset_per_duration = int(self.frame.parent.Frequency * self.frame.parent.duration)
		def __del__(self):
			self.quit()
			self.deleteLater()
		def run(self):
		#	while self.frame.parent.preload:
			preload_duration_num = math.ceil(self.frame.parent.TimeScale*0.5/self.frame.parent.duration)
			start = int(self.frame.parent.playtime/self.frame.parent.duration)
			end = math.ceil((self.frame.parent.playtime+self.frame.parent.TimeScale)/(self.frame.parent.duration))
			for i in range(preload_duration_num):
				if start-(i+1) >=0 and self.frame.parent.ck_load[start-(i+1)] == 0:
					xdata1 = list(range(int((start-(i+1))*self.frame.parent.duration*self.frame.parent.Frequency),
									int((start-i)*self.frame.parent.duration*self.frame.parent.Frequency)))
					for ch in range(self.frame.parent.Ch_num):
						ch_index = self.frame.parent.Selected_Channels_index[ch]
						ydata1 = self.frame.parent.EDF.readSignal(ch_index,xdata1[0],self.offset_per_duration)
						print(xdata1,ydata1)
						self.frame.parent.plots[start-(i+1)].append(self.frame.SignalPlot.plot(xdata1,ydata1+ch*100))
					self.frame.parent.ck_load[start-(i+1)] = 1
				
				if end+i+1 <= len(self.frame.parent.ck_load) and self.frame.parent.ck_load[start-(i+1)] == 0:
					print('Preload')
					print(end,i)
					xdata2 = list(range(int((end+(i))*self.frame.parent.duration*self.frame.parent.Frequency),
									int((end+(i+1))*self.frame.parent.duration*self.frame.parent.Frequency)))
					for ch in range(self.frame.parent.Ch_num):
						print(xdata2)
						ch_index = self.frame.parent.Selected_Channels_index[ch]
						ydata2 = self.frame.parent.EDF.readSignal(ch_index,xdata2[0],self.offset_per_duration)
						print(ydata2)
						ydata2 = ydata2+ch*100
						print(ydata2)
						self.frame.parent.plots[end+i].append(self.frame.SignalPlot.plot(xdata2,ydata2))

					self.frame.parent.ck_load[end+i] = 1
				#self.frame.parent.preload = False
	

	class UpdateThread(QThread):
		def __init__(self,parent=None):
			super(UpdateThread,self).__init__(parent)
			self.frame = parent
			self.i = i
			self.offset_per_duration = int(self.frame.parent.Frequency * self.frame.parent.duration)
		
		def __del__(self):
			self.quit()
			self.deleteLater()

		def run(self):
			#while self.frame.parent.update:
			start = int(self.frame.parent.playtime/self.frame.parent.duration)
			end = math.ceil((self.frame.parent.playtime+self.frame.parent.TimeScale)/(self.frame.parent.duration))
			for i in range(start,end):
				if self.frame.parent.ck_load[i] == 0:	
					xdata = list(range(int(i*self.frame.parent.duration * self.frame.parent.Frequency),
										int((i+1)*self.frame.parent.duration * self.frame.parent.Frequency)))
					for ch in range(self.frame.parent.Ch_num):
						ch_index = self.frame.parent.Selected_Channels_index[ch]
						ydata = self.frame.parent.EDF.readSignal(ch_index,xdata[0],self.offset_per_duration)
						self.frame.parent.plots[i].append(self.frame.SignalPlot.plot(xdata,ydata+ch*100))

					self.frame.parent.ck_load[i] = 1

				#self.frame.parent.update = False




	"""
	def PlayTimeUpdated(self):
		"""
		if self.parent.btn_click or abs(self.parent.LoadingPivot-self.parent.playtime) >= 600:
			self.SignalPlot.setXRange(self.parent.playtime*self.parent.Frequency,(self.parent.playtime + self.parent.TimeScale)*self.parent.Frequency,padding=0)
		if abs(self.parent.LoadingPivot-self.parent.playtime) >= 600:
			UpdateData(self)
		"""
		#self.SignalPlot.setXRange(self.parent.playtime*self.parent.Frequency,(self.parent.playtime+self.parent.TimeScale)*self.parent.Frequency,padding=0)
		








	#def TimeScaleUpdate(self):

	
	def viewrange_changed(self):
		#self.frame.parent.update = True
		#self.frame.parent.preload = True
		#self.frame.parent.remove = True
		self.frame.update.start()
		self.frame.remove.start()
		self.frame.preload.start()
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

		

	self.remove = RemoveThread(parent = self)
	self.preload = PreloadThread(parent = self)
	self.update = UpdateThread(parent=self)
	
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
			self.Main.SignalFrame.setGeometry(0,0,self.Main.geometry().width(),self.Main.geometry().height()*0.8)
			mkSignalWindow(self.Main.SignalFrame)
			
			self.Main.SignalFrame.show()

			
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
	

	
















