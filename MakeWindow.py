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
<<<<<<< Updated upstream
=======
import memotable as memo

class regionlinelabel(pg.InfLineLabel):
	def __init__(self, line, main,text="", movable=False, position=0.8, anchors=None, **kwds):
		self.line = line
		self.movable = movable
		self.moving = False
		self.orthoPos = position  # text will always be placed on the line at a position relative to view bounds
		self.format = text
		self.have_a_pole = False
		self.line.sigPositionChanged.connect(self.valueChanged)
		self._endpoints = (None, None)
		
		if anchors is None:
			# automatically pick sensible anchors
			rax = kwds.get('rotateAxis', None)
			if rax is not None:
				if tuple(rax) == (1,0):
					anchors = [(0.5, 0), (0.5, 1)]
				else:
					anchors = [(0, 0.5), (1, 0.5)]
			else:
				if line.angle % 180 == 0:
					anchors = [(0.5, 0), (0.5, 1)]
				else:
					anchors = [(0, 0.5), (1, 0.5)]
			
		self.anchors = anchors
		pg.TextItem.__init__(self, **kwds)
		self.setParentItem(line)
		self.main = main
		self.setColor('#FFFFFF')

		self.valueChanged()
		
	def valueChanged(self):
		if not self.isVisible():
			return
		value = self.line.value()
		self.format = '%02d:%02d:%02d.%02d'%((value/self.main.Frequency)//3600,(value/self.main.Frequency)%3600//60,(value/self.main.Frequency)%60//1,(value/self.main.Frequency)%1*100//1)
		self.setText(self.format.format(value=value))
		self.updatePosition()



class mkrbtnlist:
	def __init__(self,main):
		self.main=main
		self.initUI()
		self.on_drag = False
		self.no_drag = True
		self.ctrl_start = False
		self.z=0
		self.start_copy = None

		
	def initUI(self):

		self.menu = QMenu()
		self.memoaction = self.menu.addAction('Memo')
		self.memoaction.triggered.connect(self.tomemo)


		self.detchangeaction = self.menu.addMenu('Change Detection Data')
		self.dettozero = self.detchangeaction.addAction('False')
		self.dettoone = self.detchangeaction.addAction('True')
		self.dettozero.triggered.connect(self.dtz)
		self.dettoone.triggered.connect(self.dto)


		self.predchangeaction = self.menu.addMenu('Change Prediction Data')
		self.predtozero = self.predchangeaction.addAction('False')
		self.predtoone = self.predchangeaction.addAction('True')
		self.predtozero.triggered.connect(self.ptz)
		self.predtoone.triggered.connect(self.pto)

		self.main.ctrl_release.connect(self.control_release)

	def tomemo(self):
		self.main.memo()
		self.main.SignalFrame.addF(self.timestart.format,self.timeend.format)
		
	def dtz(self):
		if self.regionstart.x() < self.regionend.x():
			start = int(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			end = math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)
		else:
			end = math.ceil(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			start = int(self.vb.mapToView(self.regionend).x()*self.main.unit)

		self.main.detData[start:end] = list(np.zeros(end-start))
		self.main.DPFrame.det.p.setData(self.main.detx,self.main.detData)
		Menuaction.detdataplot(self.main)
	def dto(self):
		if self.regionstart.x() < self.regionend.x():
			start = int(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			end = math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)
		else:
			end = math.ceil(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			start = int(self.vb.mapToView(self.regionend).x()*self.main.unit)

		self.main.detData[start:end] = list(np.ones(end-start))
		self.main.DPFrame.det.p.setData(self.main.detx,self.main.detData)
		Menuaction.detdataplot(self.main)
	def ptz(self):
		if self.regionstart.x() < self.regionend.x():
			start = int(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			end = math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)
		else:
			end = math.ceil(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			start = int(self.vb.mapToView(self.regionend).x()*self.main.unit)

		self.main.predData[start:end] = list(np.zeros(end-start))
		self.main.DPFrame.pred.pr.setData(self.main.predx,-self.main.predData)
		Menuaction.preddataplot(self.main)
	def pto(self):
		if self.regionstart.x() < self.regionend.x():
			start = int(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			end = math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)
		else:
			end = math.ceil(self.vb.mapToView(self.regionstart).x()*self.main.unit)
			start = int(self.vb.mapToView(self.regionend).x()*self.main.unit)

		self.main.predData[start:end] = list(np.ones(end-start))
		self.main.DPFrame.pred.pr.setData(self.main.predx,-self.main.predData)
		Menuaction.preddataplot(self.main)

	def menupopup(self):
		mousepos = win32api.GetCursorPos()
		pos = QPoint(int(mousepos[0]),int(mousepos[1]))
		self.menu.popup(pos)

	def press(self,ev):
		#region 생성
		if self.no_drag:
			frame = self.main.SignalFrame
			self.vb = frame.PlotViewBox
			
			self.region=pg.LinearRegionItem()
			self.main.SignalFrame.SignalPlot.addItem(self.region)
			self.region.setMovable(False)

			self.outregion=pg.LinearRegionItem()
			self.main.SignalFrame.SignalPlot.addItem(self.outregion)
			self.outregion.setMovable(False)

			self.timestart = regionlinelabel(self.region.lines[0],self.main)
			self.timeend = regionlinelabel(self.region.lines[1],self.main)
			self.outstart = regionlinelabel(self.outregion.lines[0],self.main)
			self.outend = regionlinelabel(self.outregion.lines[1],self.main)

			self.timestart.setPosition(0.45)
			self.timeend.setPosition(0.45)
			self.outstart.setPosition(0.55)
			self.outend.setPosition(0.55)

			self.region.setBrush((218, 230, 228,20))
			self.region.lines[0].setPen(pg.mkPen(color=(218, 230, 228,20),width=1))
			self.region.lines[1].setPen(pg.mkPen(color=(218, 230, 228,20),width=1))
			self.outregion.setBrush((218, 230, 228,20))				
			self.outregion.lines[0].setPen(pg.mkPen(color=(218, 230, 228,20),width=1))
			self.outregion.lines[1].setPen(pg.mkPen(color=(218, 230, 228,20),width=1))

			self.no_drag = False


		if ev.buttons() == Qt.LeftButton:
			self.mousePress = True
			self.regionstart = ev.pos()

			if self.main.SignalFrame.PlotViewBox.CtrlPress == True :


				if self.ctrl_start == False:
					self.ctrl_start = True

				self.regionend = ev.pos()
				if self.start_copy == None:
					self.start_copy = self.vb.mapToView(self.regionstart)

				if self.start_copy.x() < self.regionend.x():

					self.region.setRegion((self.start_copy.x(),self.vb.mapToView(self.regionend).x()))	
					self.outregion.setRegion((int(self.start_copy.x()*self.main.unit)*self.main.Frequency,
												math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)*self.main.Frequency))
				else:
					self.region.setRegion((self.vb.mapToView(self.regionend).x(),self.start_copy.x()))
					self.outregion.setRegion((int(self.vb.mapToView(self.regionend).x()*self.main.unit)*self.main.Frequency,
											math.ceil(self.start_copy.x()*self.main.unit)*self.main.Frequency))
					

			elif self.main.SignalFrame.PlotViewBox.CtrlPress == False:
				self.region.setRegion((self.vb.mapToView(self.regionstart).x(),self.vb.mapToView(self.regionstart).x()))
				self.outregion.setRegion((int(self.vb.mapToView(self.regionstart).x()*self.main.unit)*self.main.Frequency,
										math.ceil(self.vb.mapToView(self.regionstart).x()*self.main.unit)*self.main.Frequency))

				
			
			if self.ctrl_start == False:
				self.start_copy = self.vb.mapToView(self.regionstart)

			self.on_drag = False

		elif ev.button() == Qt.RightButton:
			if self.on_drag and (self.z > 0.03):
				self.detchangeaction.setEnabled(True)
				self.predchangeaction.setEnabled(True)
				self.menupopup()
			else:
				self.detchangeaction.setEnabled(False)
				self.predchangeaction.setEnabled(False)
				self.menupopup()

		
	def move(self,ev):
		if self.main.SignalFrame.PlotViewBox.CtrlPress == False:
			if self.mousePress:
				if ev.buttons() == Qt.LeftButton:
					self.regionend = ev.pos()
					self.on_drag = True
					if self.regionstart.x() < self.regionend.x():

						self.region.setRegion((self.vb.mapToView(self.regionstart).x(),self.vb.mapToView(self.regionend).x()))	
						self.outregion.setRegion((int(self.vb.mapToView(self.regionstart).x()*self.main.unit)*self.main.Frequency,
													math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)*self.main.Frequency))
					else:
						self.region.setRegion((self.vb.mapToView(self.regionstart).x(),self.vb.mapToView(self.regionend).x()))	
						self.outregion.setRegion((math.ceil(self.vb.mapToView(self.regionstart).x()*self.main.unit)*self.main.Frequency,
													int(self.vb.mapToView(self.regionend).x()*self.main.unit)*self.main.Frequency))
			
		elif self.main.SignalFrame.PlotViewBox.CtrlPress == True:
			if self.mousePress:
				if ev.buttons() == Qt.LeftButton:
					self.regionend = ev.pos()
					self.on_drag = True
					if self.start_copy.x() < self.regionend.x():

						self.region.setRegion((self.start_copy.x(),self.vb.mapToView(self.regionend).x()))	
						self.outregion.setRegion((int(self.start_copy.x()*self.main.unit)*self.main.Frequency,
													math.ceil(self.vb.mapToView(self.regionend).x()*self.main.unit)*self.main.Frequency))
					else:
						self.region.setRegion((self.vb.mapToView(self.regionend).x(),self.start_copy.x()))
						self.outregion.setRegion((int(self.vb.mapToView(self.regionend).x()*self.main.unit)*self.main.Frequency,
												math.ceil(self.start_copy.x()*self.main.unit)*self.main.Frequency))
		self.z = abs(self.vb.mapToView(self.regionstart).x()-self.vb.mapToView(self.regionend).x())

	def release(self,ev):
		if ev.buttons() == Qt.LeftButton:
			self.mousePress = False
	def control_release(self):
		self.ctrl_start = False


>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======
				"""
				
				childwidget.setGeometry((self.ChildrenWidget_baseSize[i][2]*xSizeChangeRatio),
									(self.ChildrenWidget_baseSize[i][3]*ySizeChangeRatio),
									math.ceil(self.ChildrenWidget_baseSize[i][0]*xSizeChangeRatio),
									math.ceil(self.ChildrenWidget_baseSize[i][1]*ySizeChangeRatio))
				i=i+1
		
		else:
			self.setChildWidgetInfo()
			self.initResized = True

class fftframe(QWidget):
	def __init__(self,parent=None):
		super(fftframe,self).__init__(parent)
		self.parent = parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.initResized = False
		self.parent.xSizeChangeRatio =1
		self.parent.ySizeChangeRatio =1
		self.fail_to_close = False

	
	def setChildWidgetInfo(self):
		self.ChildrenWidget = []

		for widget in self.findChildren(QWidget):
			self.ChildrenWidget.append(widget)

		
		self.FrameSize_width = self.geometry().width()
		self.FrameSize_height = self.geometry().height()

		self.ChildrenWidget_baseSize = []
		for childwidget in self.ChildrenWidget:
			#self.ChildrenWidget_baseSize.append([childwidget.size().width(),childwidget.size().height()])

			self.ChildrenWidget_baseSize.append([childwidget.geometry().width() if childwidget.geometry().width()!=0 else 1,
												childwidget.geometry().height() if childwidget.geometry().height()!=0 else 1,
												childwidget.geometry().x(),
												childwidget.geometry().y()])


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
			self.parent.xSizeChangeRatio = (1+(self.geometry().width() - self.FrameSize_width ) / self.FrameSize_width)
			self.parent.ySizeChangeRatio = (1+(self.geometry().height() - self.FrameSize_height )/ self.FrameSize_height)
			i=0

			for childwidget in self.ChildrenWidget:
				if str(type(childwidget)) == "<class 'show_fft_function.scalebutton'>":
					childwidget.setGeometry((self.ChildrenWidget_baseSize[i][2]*self.parent.xSizeChangeRatio),
										(self.geometry().height()-30),
										math.ceil(self.ChildrenWidget_baseSize[i][0]*self.parent.xSizeChangeRatio),
										math.ceil(self.ChildrenWidget_baseSize[i][1]*self.parent.ySizeChangeRatio))
				else:
					childwidget.setGeometry((self.ChildrenWidget_baseSize[i][2]*self.parent.xSizeChangeRatio),
										(self.ChildrenWidget_baseSize[i][3]*self.parent.ySizeChangeRatio),
										math.ceil(self.ChildrenWidget_baseSize[i][0]*self.parent.xSizeChangeRatio),
										math.ceil(self.ChildrenWidget_baseSize[i][1]*self.parent.ySizeChangeRatio))
				i=i+1
		
>>>>>>> Stashed changes
		else:
			self.setChildWidgetInfo()
			self.initResized = True
	
<<<<<<< Updated upstream




=======
class signalframe(QWidget):
	def __init__(self,parent=None):
		super(signalframe,self).__init__(parent)
		self.parent = parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.initResized = False
		self.rbtnlist = mkrbtnlist(self.parent)
		self.msgbox = QMessageBox(self)
		self.parent.sigexist = True
		self.fail_to_close = False
	
	def setChildWidgetInfo(self):
		self.ChildrenWidget = []

		for widget in self.findChildren(QWidget):
			if not 'label' in str(widget).lower():
				self.ChildrenWidget.append(widget)

		
		self.FrameSize_width = self.frameGeometry().width()
		self.FrameSize_height = self.frameGeometry().height()

		self.ChildrenWidget_baseSize = []
		for childwidget in self.ChildrenWidget:
			#self.ChildrenWidget_baseSize.append([childwidget.size().width(),childwidget.size().height()])
			self.ChildrenWidget_baseSize.append([childwidget.size().width() if childwidget.size().width()!=0 else 1,
												childwidget.size().height() if childwidget.size().height()!=0 else 1,
												childwidget.geometry().x(),
												childwidget.geometry().y()])

	def closeEvent(self,e):
		self.parent.memobox.close()
		ok = self.msgbox.question(self, 'Save', 'Save All Changes?', QMessageBox.Yes | QMessageBox.No)
		if ok:
			

			headers = ['det','pred']
			df = pd.DataFrame(list(zip(self.parent.detData,self.parent.predData)),columns=headers)
			if hasattr(self.parent,'dpPath'):
				df.to_csv(self.parent.dpPath,mode='w',index=False)
			else:
				df.to_csv('./detpred/'+'dp_'+self.parent.edfname[:-4]+'_save'+'.csv',mode='w',index=False)
			a = self.saveF()
			if a==-1:
				self.fail_to_close=True
				e.ignore()
			else:
				self.fail_to_close=False

			self.parent.sigexist=False
		self.deleteLater()



	def nativeEvent(self,eventType,message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if eventType == "windows_generic_MSG":
			if msg.message == win32con.WM_NCLBUTTONDOWN:
				nHittest = int(msg.wParam)
				if nHittest in [win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
					self.setChildWidgetInfo()

		return False, 0
			
	def resizeEvent(self,e):
		xSizeChangeRatio =1
		ySizeChangeRatio =1
		if self.initResized:
			xSizeChangeRatio = (1+(e.size().width() - self.FrameSize_width ) / self.FrameSize_width)
			ySizeChangeRatio = (1+(e.size().height() - self.FrameSize_height )/ self.FrameSize_height)
			i=0
			for childwidget in self.ChildrenWidget:
				
				#childwidget.resize(self.ChildrenWidget_baseSize[i][0]*xSizeChangeRatio, self.ChildrenWidget_baseSize[i][1]*ySizeChangeRatio)
				#i=i+1

				
				childwidget.setGeometry((self.ChildrenWidget_baseSize[i][2]*xSizeChangeRatio),
									(self.ChildrenWidget_baseSize[i][3]*ySizeChangeRatio),
									math.ceil(self.ChildrenWidget_baseSize[i][0]*xSizeChangeRatio),
									math.ceil(self.ChildrenWidget_baseSize[i][1]*ySizeChangeRatio))
				i=i+1



		else:
			self.setChildWidgetInfo()
			self.initResized = True
	
>>>>>>> Stashed changes

def mkSignalWindow(self):

	def viewbox_resized(viewbox):
		viewbox_pos_x = viewbox.geometry().x()
		viewbox_pos_y = viewbox.geometry().y()
		viewbox_height = viewbox.size().height()
		main_height = self.parent.geometry().height()
		space = viewbox_height/(self.parent.Ch_num+1)
		if not self.parent.Resized:
<<<<<<< Updated upstream
			viewbox_pos_x = viewbox.geometry().x()
			viewbox_pos_y = viewbox.geometry().y()
			viewbox_height = viewbox.size().height()

			margin = (self.SignalPlot.geometry().height() - viewbox_height)/2
			LabelBox = QVBoxLayout()
			LabelBox.setContentsMargins(20,5+self.SignalPlot.geometry().y()+margin,0,self.geometry().height()-self.SignalPlot.geometry().height()+margin)
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

		

=======
			self.lbl_list = []
			for i in range(self.parent.Ch_num):
				lbl = QLabel(parent=self)
				self.lbl_list.append(lbl)
				lbl.setText(self.parent.Selected_Chs[self.parent.Ch_num - i - 1])
				lbl.setGeometry(10,(viewbox_pos_y+10)+(i+1)*space-8,50,20)
				lbl.setMaximumHeight(16)
				lbl.setMinimumHeight(16)
				lbl.setWindowFlags(Qt.WindowStaysOnTopHint)
				lbl.setFixedWidth(lbl.sizeHint().width())
				lbl.setScaledContents(True)
				lbl.setStyleSheet('color:yellow; background:#333333')
				lbl.show()
>>>>>>> Stashed changes

			self.parent.Resized = True
		else:
			for i in range(len(self.lbl_list)):
				self.lbl_list[i].setGeometry(10,(viewbox_pos_y+10)+(i+1)*space-8,50,20)
				self.lbl_list[i].updateGeometry()

	self.parent.signal_frame_width = self.frameGeometry().width()
	self.parent.signal_frame_height = self.frameGeometry().height()

	pg.setConfigOption('background', '#333333')
	pg.setConfigOption('foreground', 'y')
	self.SignalWindow = pg.GraphicsLayoutWidget(parent=self)
	self.dragging = False
	
	self.SignalWindow.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
	self.SignalWindow.setGeometry(0,0,self.parent.signal_frame_width,self.parent.signal_frame_height)
	
	class TimeAxisItem(pg.AxisItem):
		def __init__(self, frame,*args, **kwargs):
			super().__init__(*args, **kwargs)
			self.enableAutoSIPrefix(False)
			self.frame = frame

		def tickStrings(self, values, scale, spacing):
			return ["%02d:%02d:%02.2f"%((local_time/self.frame.parent.Frequency)/3600,((local_time/self.frame.parent.Frequency)%3600)/60,((local_time/self.frame.parent.Frequency)%3600%60)) for local_time in values]

	self.axisitem = TimeAxisItem(self,orientation='bottom')

	self.SignalPlot = self.SignalWindow.addPlot(enableMenu = False,enableMouse=False,row=0,col=0,colspan=9,axisItems={'bottom':self.axisitem},
												border=pg.mkPen(color=(255,255,0,255),width=4))



	self.SignalPlot.showButtons()

	#self.SignalPlot.setBackground('w')
	
	self.SignalPlot.setContentsMargins(0, 0, 0, 0)
	
	plotstyle = pg.mkPen(color='y',width=0.6)
	self.SignalPlot.hideAxis('left')
	#self.SignalPlot.hideAxis('bottom')
	self.SignalPlot.setXRange(0,self.parent.TimeScale*(self.parent.Frequency),padding=0)
	self.SignalPlot.setYRange(-100,(self.parent.Ch_num-1)*100+100,padding=0)
	self.SignalPlot.enableAutoRange(axis='xy',enable=False)
	self.SignalPlot.setMouseEnabled(x=True,y=True)
	self.SignalPlot.setDownsampling(ds = self.parent.ds,auto=False,mode='subsample')

	self.SignalPlot.setClipToView(True)

	#self.SignalPlot.addLine(x=line)
#	pg.setConfigOption('wheelspin',False)
	self.parent.plotdic=[]
	self.parent.linedic=[]
	self.parent.PlotData={'x' : [], 'y' : []}
	
	
	for i in range(self.parent.Ch_num):
		self.parent.plotdic.append(self.SignalPlot.plot(pen=plotstyle, name=str(i)))
		self.parent.PlotData['x'].append(list(range(0,20*self.parent.Frequency)))
		self.parent.PlotData['y'].append(self.parent.EDF.readSignal(self.parent.Selected_Channels_index[i],self.parent.playtime*self.parent.Frequency,20*self.parent.Frequency)+i*100)
		line = pg.InfiniteLine(pen=pg.mkPen((255,255,255,30),width=1),angle=0,pos=i*100)
		self.SignalPlot.addItem(line)
		self.parent.plotdic[i].setData(self.parent.PlotData['x'][i],self.parent.PlotData['y'][i])
		if i==0:
			self.parent.plotdic[i].start_duration = 0
			self.parent.plotdic[i].end_duration = int(20/self.parent.duration)
	for i in range(math.ceil(20/self.parent.duration)):
		self.parent.ck_load[i] = 1

	a = self.parent.plotdic[self.parent.Ch_num-1]
	for i in range(20):
		line = pg.InfiniteLine(pen=pg.mkPen((255,255,255,70),width=0.8),angle=90,pos=int(i*self.parent.Frequency))
		line.time = i
		self.SignalPlot.addItem(line)
		

	self.PlotViewBox = self.SignalPlot.getViewBox()
	self.PlotViewBox.enableMenu = False
	self.parent.viewbox_exist = True
	self.PlotViewBox.border = pg.mkPen(color=(255,255,255,150),width=0.8)
	self.PlotViewBox.frame = self
	
	self.PlotViewBox.setLimits(xMin=0,yMin=-100,yMax=(self.parent.Ch_num-1)*100+100,
								minYRange = (self.parent.Ch_num-1)*100+200,maxYRange=(self.parent.Ch_num-1)*100+200
								,minXRange=self.parent.Frequency*0.1,maxXRange=self.parent.Frequency*602)
	self.parent.Resized = False


	# Move event trigger
	proxy = QGraphicsProxyWidget()
<<<<<<< Updated upstream
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
=======
	button_left = QPushButton("<")
	button_left.setMaximumWidth(self.parent.signal_frame_width//32)

	proxy2 = QGraphicsProxyWidget()
	button_right = QPushButton('>')
	button_right.setMaximumWidth(self.parent.signal_frame_width//32)

	proxy3 = QGraphicsProxyWidget()
	button_right_u = QPushButton('>>')
	button_right_u.setMaximumWidth(self.parent.signal_frame_width//32)

	proxy4 = QGraphicsProxyWidget()
	button_left_u = QPushButton("<<")
	button_left_u.setMaximumWidth(self.parent.signal_frame_width//32)

>>>>>>> Stashed changes

	textproxy = QGraphicsProxyWidget()
	self.textbox1 = QLineEdit()
	self.textbox1.setAlignment(Qt.AlignCenter)

	textproxy2 = QGraphicsProxyWidget()
	self.textbox2 = QLineEdit()
	self.textbox2.setAlignment(Qt.AlignCenter)
	
	self.textbox1.setText("%d:%d:%.2f"%(self.parent.playtime//3600,(self.parent.playtime%3600)//60,((self.parent.playtime)%3600)%60))
	self.textbox2.setText("%d:%d:%.2f"%((self.parent.playtime+self.parent.TimeScale)//3600,((self.parent.playtime+self.parent.TimeScale)%3600)//60,((self.parent.playtime+self.parent.TimeScale)%3600)%60))
<<<<<<< Updated upstream
=======
	self.textbox3.setText('Timescale: %.2f sec'%(self.parent.TimeScale) if self.parent.TimeScale//60 == 0 else 'Timescale: %dmin %dsec'%(self.parent.TimeScale/60,self.parent.TimeScale%60))
>>>>>>> Stashed changes


	
	proxy.setWidget(button_left_u)
	proxy2.setWidget(button_left)
	proxy3.setWidget(button_right)
	proxy4.setWidget(button_right_u)
	textproxy.setWidget(self.textbox1)
	textproxy2.setWidget(self.textbox2)

<<<<<<< Updated upstream
	self.TestButton = self.SignalWindow.addLayout(row=2,col=0)
	self.spaceLayout = self.SignalWindow.addLayout(row=2,col=1,colspan=8)
	self.spaceLayout.setMaximumHeight(40)
	self.TestButton.setMaximumHeight(40)
	self.TestButton.setMaximumWidth(160)
=======
	self.TestButton = self.SignalWindow.addLayout(row=3,col=0)
	self.spaceLayout = self.SignalWindow.addLayout(row=3,col=1,colspan=3)
	self.spaceLayout.setMaximumHeight(30)
	self.TestButton.setMaximumHeight(30)
	self.TestButton.setMaximumWidth(self.parent.signal_frame_width//8)
>>>>>>> Stashed changes
	self.TestButton.addItem(proxy)
	self.TestButton.addItem(proxy2)
	self.TestButton.addItem(proxy3)
	self.TestButton.addItem(proxy4)
<<<<<<< Updated upstream
	self.textlayout = self.SignalWindow.addLayout(row=1,col=0)
	self.spacelayout = self.SignalWindow.addLayout(row=1,col=1,colspan=7)
	self.spacelayout.setMaximumHeight(40)
	self.textlayout2= self.SignalWindow.addLayout(row=1,col=8)
	self.textlayout.setMaximumHeight(40)
	self.textlayout.setMaximumWidth(100)
	self.textlayout2.setMaximumHeight(40)
	self.textlayout2.setMaximumWidth(100)
=======

	self.textlayout = self.SignalWindow.addLayout(row=2,col=0)
	self.spacelayout = self.SignalWindow.addLayout(row=2,col=1,colspan=3)
	self.spacelayout.setMaximumHeight(30)

	self.textlayout3= self.SignalWindow.addLayout(row=2,col=4)

	self.spacelayout = self.SignalWindow.addLayout(row=2,col=5,colspan=3)
	self.spacelayout.setMaximumHeight(30)

	self.textlayout2= self.SignalWindow.addLayout(row=2,col=8)

	self.textlayout.setMaximumHeight(30)
	self.textlayout.setMaximumWidth(self.parent.signal_frame_width//8)
	self.textlayout2.setMaximumHeight(30)
	self.textlayout2.setMaximumWidth(self.parent.signal_frame_width//8)
	self.textlayout3.setMaximumHeight(30)
	self.textlayout3.setMaximumWidth(self.parent.signal_frame_width//8)
>>>>>>> Stashed changes
	self.textlayout.addItem(textproxy)
	self.textlayout2.addItem(textproxy2)

	#self.textlayout.setMaximumWidth(100)
	#self.textlayout2.setMaximumWidth(100)

	
	self.SignalWindow.show()

	###########        Update Thread         #################
	class Update(QObject):
		def __init__(self,parent=None):
			super(Update,self).__init__(None)
			self.frame = parent

		def StartUpdate(self,direction):
			i=0
			pen = pg.mkPen(color='y',width=0.5)
			#처음 끝 계산
			
			#진행방향 앞쪽
			if direction == 1:
				current_duration_index = int((self.frame.parent.playtime)/self.frame.parent.duration)
				while True:
					if self.frame.parent.ck_load[current_duration_index + i] == 0:
						start_duration_index = current_duration_index + i
	
						break
					i = i + 1
				start = int(start_duration_index * self.frame.parent.duration * self.frame.parent.Frequency)
				
				if self.frame.parent.duration * self.frame.parent.EDF.datarecords_in_file < self.frame.parent.playtime+self.frame.parent.TimeScale*2:
					end = int(self.frame.parent.duration * self.frame.parent.EDF.datarecords_in_file * self.frame.parent.Frequency)
				else:
					end = int((self.frame.parent.playtime+self.frame.parent.TimeScale*2) * self.frame.parent.Frequency)
				
				end_duration_index = int(end/(self.frame.parent.Frequency*self.frame.parent.duration))
				end = int((end_duration_index+1) * self.frame.parent.duration * self.frame.parent.Frequency)
			#진행방향 뒤쪽
			if direction == 0:
				current_duration_index = math.ceil((self.frame.parent.playtime)/self.frame.parent.duration)
				while True:
					if self.frame.parent.ck_load[current_duration_index - i] == 0:
						end_duration_index = current_duration_index - i
						break
					i = i +1
				end = math.ceil((end_duration_index+1) * self.frame.parent.duration * self.frame.parent.Frequency)
				if 0 > self.frame.parent.playtime-self.frame.parent.TimeScale:
					start = 0
				else:
					start = int((self.frame.parent.playtime-self.frame.parent.TimeScale) * self.frame.parent.Frequency)
				
				start_duration_index = int(start/(self.frame.parent.Frequency*self.frame.parent.duration))
				if start_duration_index < 0 :
					start_duration_index = 0
				start = int(start_duration_index * self.frame.parent.duration * self.frame.parent.Frequency)

<<<<<<< Updated upstream
 			######################   플로팅   ##########################
=======
			######################	플로팅	##########################
			data_total = 0
			plot_total = 0
>>>>>>> Stashed changes
			if start < end:
				xdata = list(range(start,end))

				for i in range(self.frame.parent.Ch_num):
					ch_index = self.frame.parent.Selected_Channels_index[i]
					
					pstart = time.time()
					ydata = (list(self.frame.parent.EDF.readSignal(ch_index,start,end-start)+i*100))
					data_total += time.time()-pstart
					
					pstart = time.time()
					inst = self.frame.SignalPlot.plot(x = xdata,y = ydata,pen=pen)
					plot_total += time.time()-pstart
					inst.start_duration = start_duration_index
					inst.end_duration = end_duration_index

				line_start = ((int(start/self.frame.parent.Frequency)//self.frame.parent.line_per_time))*self.frame.parent.line_per_time
				line_end = (math.ceil(math.ceil(((end)/self.frame.parent.Frequency))/self.frame.parent.line_per_time))*self.frame.parent.line_per_time
				line_pos = line_start
				while line_end > line_pos :
					line = pg.InfiniteLine(pen=pg.mkPen((255,255,255,100),width=0.8),angle=90,pos=line_pos*self.frame.parent.Frequency)
					self.frame.SignalPlot.addItem(line)
					line.time = line_pos
					line_pos = line_pos + self.frame.parent.line_per_time


			
				for i in range(start_duration_index,end_duration_index+1):
					self.frame.parent.ck_load[i] = 1
			##### 삭제 ####	
			itemlist = self.frame.SignalPlot.allChildItems()
			for i in range(int(len(itemlist))):
				if hasattr(itemlist[i],'start_duration'):
					s = itemlist[i].start_duration
					e = itemlist[i].end_duration + 1
					if (e < math.ceil(((self.frame.parent.playtime - self.frame.parent.TimeScale)/self.frame.parent.duration)) or 
						s > ((self.frame.parent.playtime + self.frame.parent.TimeScale*2)/self.frame.parent.duration)):
						self.frame.SignalPlot.removeItem(itemlist[i])
						for j in range(s,e):
							self.frame.parent.ck_load[j] = 0
						
				if hasattr(itemlist[i],'time'):
					if (self.frame.parent.playtime - self.frame.parent.TimeScale*2) > itemlist[i].time or (self.frame.parent.playtime + self.frame.parent.TimeScale*3) < itemlist[i].time:
						self.frame.SignalPlot.removeItem(itemlist[i])


					
	class LineUpdate(QObject):
		def __init__(self,parent=None):
			super(LineUpdate,self).__init__(None)
			self.frame = parent
		def lineupdate(self):
			itemlist = self.frame.SignalPlot.allChildItems()
			for item in itemlist:
				if hasattr(item,'time'):
					self.frame.SignalPlot.removeItem(item)

			start = self.frame.parent.playtime - self.frame.parent.TimeScale
			if start < 0:
				start = 0
			start = (start//self.frame.parent.line_per_time)*self.frame.parent.line_per_time
			end  = (self.frame.parent.playtime + self.frame.parent.TimeScale*2)
			if end > self.frame.parent.duration*self.frame.parent.EDF.datarecords_in_file:
				end = self.frame.parent.duration*self.frame.parent.EDF.datarecords_in_file-1
			end = (end//self.frame.parent.line_per_time)*self.frame.parent.line_per_time
			while start < end:
				line = pg.InfiniteLine(pen=pg.mkPen((255,255,255,100),width=0.8),angle=90,pos=start*self.frame.parent.Frequency)
				line.time = start
				self.frame.SignalPlot.addItem(line)
				start = start + self.frame.parent.line_per_time
		

	self.UpdatePlotting = Update(self)
	self.LineUpdatting = LineUpdate(self)
	self.UpdateThread = QThread()
	self.LineThread = QThread()
	self.UpdatePlotting.moveToThread(self.UpdateThread)
	self.LineUpdatting.moveToThread(self.LineThread)
	self.UpdateThread.start()
	self.LineThread.start()


	def PlayTimeUpdated(self):
		if self.parent.btn_click or abs(self.parent.LoadingPivot-self.parent.playtime) >= self.parent.TimeScale or (not self.PlotViewBox.CtrlPress):
			self.SignalPlot.setXRange(self.parent.playtime*self.parent.Frequency,(self.parent.playtime + self.parent.TimeScale)*self.parent.Frequency,padding=0,update=True)				
		if abs(self.parent.LoadingPivot-self.parent.playtime) >= self.parent.TimeScale:
			#0 == 진행방향 뒤로 , 1== 진행방향 앞으로
			if self.parent.jump:
				self.UpdatePlotting.StartUpdate(0)
				self.UpdatePlotting.StartUpdate(1)
				self.parent.jump=False
			else:
				if self.parent.LoadingPivot-self.parent.playtime < 0:
					direction = 1
				else:
					direction = 0
				self.UpdatePlotting.StartUpdate(direction)
			self.parent.LoadingPivot = self.parent.playtime
		
		#self.SignalPlot.setXRange(self.parent.playtime*self.parent.Frequency,(self.parent.playtime+self.parent.TimeScale)*self.parent.Frequency,padding=0)
		self.parent.DPFrame.getPlaytimeChanged(self.parent.playtime)
		self.textbox1.setText("%d:%d:%.2f"%(self.parent.playtime//3600,(self.parent.playtime%3600)//60,((self.parent.playtime)%3600)%60))
		self.textbox2.setText("%d:%d:%.2f"%((self.parent.playtime+self.parent.TimeScale)//3600,((self.parent.playtime+self.parent.TimeScale)%3600)//60,
			((self.parent.playtime+self.parent.TimeScale)%3600)%60))
<<<<<<< Updated upstream

=======
		self.textbox3.setText('Timescale: %.2f sec'%(self.parent.TimeScale) if self.parent.TimeScale//60 == 0 else 'Timescale: %dmin %dsec'%(self.parent.TimeScale/60,self.parent.TimeScale%60))
			
		if not self.sb.isSliderDown():
			self.sb.setSliderPosition(self.parent.playtime)
>>>>>>> Stashed changes
	# self = button 클래스임
	def viewrange_changed(self):
		cur_TimeScale = ((self.viewRange()[0][1]-self.viewRange()[0][0])/self.frame.parent.Frequency)//self.frame.parent.unit/self.frame.parent.Frequency
		if abs(cur_TimeScale - self.frame.parent.TimeScale) > 1/self.frame.parent.Frequency*4:
			if self.frame.parent.TimeScale >= 300 and not self.frame.parent.line_per_time == 120:
				self.frame.parent.line_per_time = 120
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 90 and not self.frame.parent.line_per_time == 60:
				self.frame.parent.line_per_time = 60
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 30 and not self.frame.parent.line_per_time == 20:
				self.frame.parent.line_per_time = 20
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 10 and not self.frame.parent.line_per_time == 5:
				self.frame.parent.line_per_time = 5
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 3 and not self.frame.parent.line_per_time == 2:
				self.frame.parent.line_per_time = 2
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 1 and not self.frame.parent.line_per_time ==0.5 :
				self.frame.parent.line_per_time = 0.5
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 0.5 and not self.frame.parent.line_per_time == 0.3:
				self.frame.parent.line_per_time = 0.3
				self.frame.LineUpdatting.lineupdate()
			elif self.frame.parent.TimeScale >= 0.1 and not self.frame.parent.line_per_time == 0.05:
				self.frame.parent.line_per_time = 0.05
				self.frame.LineUpdatting.lineupdate()
			self.frame.dragging = True
			self.frame.parent.TimeScale = cur_TimeScale
		else:
			self.frame.SignalPlot.setXRange(self.frame.parent.playtime*self.frame.parent.Frequency,(self.frame.parent.playtime + self.frame.parent.TimeScale)*self.frame.parent.Frequency,padding=0,update=True)
		
		

		if not self.frame.parent.ds == 4+self.frame.parent.TimeScale//50:
			self.frame.parent.ds = 4+self.frame.parent.TimeScale//50
			self.frame.SignalPlot.setDownsampling(ds=self.frame.parent.ds)
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
		def closeEvent(self,ev):
			self.deleteLater()
			if not self.Main.ChannelOpen:
				self.Main.EDF._close()


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
<<<<<<< Updated upstream
											self.Main.geometry().height()*0.8-20)
=======
											self.Main.geometry().height()*0.88-self.Main.menubar.height())
>>>>>>> Stashed changes
			self.Main.DPNameFrame.setGeometry(0,
<<<<<<< HEAD
											self.Main.geometry().height()*0.88,
											self.Main.geometry().width()*1/24,
											self.Main.geometry().height()*0.12)
			self.Main.DPFrame.setGeometry(self.Main.geometry().width()*1/24,
										self.Main.geometry().height()*0.88,
										self.Main.geometry().width()*23/24,
										self.Main.geometry().height()*0.12)
=======
											self.Main.geometry().height()*0.8,
											self.Main.geometry().width()*1/25,
											self.Main.geometry().height()*0.2)
			self.Main.DPFrame.setGeometry(self.Main.geometry().width()*1/25,
										self.Main.geometry().height()*0.8,
										self.Main.geometry().width()*24/25,
										self.Main.geometry().height()*0.2)
>>>>>>> parent of f499a00... Merge branch 'design' into Thisss
			mkSignalWindow(self.Main.SignalFrame)
			timelinetest.detPredBar(self.Main.DPFrame)
			timelinetest.dfname(self.Main.DPNameFrame)
	
			self.Main.SignalFrame.show()
			self.Main.DPFrame.show()
			self.Main.DPNameFrame.show()
		
			
			self.close()
			


		def Cancel(self):
			
			self.close()


			
		def initUI(self):
			self.Main.ChannelOpen = False
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
	

	
















