import sys
import types
import os
import ctypes
import pyedflib
import pyqtgraph as pg
import win32api
import win32con
import win32gui
import time
import inspect
import ctypes.wintypes
import numpy as np

from functools import partial
from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager,NamespaceProxy
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ctypes.wintypes import POINT

import Menuaction
import MakeWindow
import show_fft_function as showfft




class EDFbrowse(QMainWindow):

	TimeScaleChanged = pyqtSignal()
	Ch_numChanged = pyqtSignal()
	playtimeChanged = pyqtSignal()

	def __init__(self,manager,parent=None):
		super(EDFbrowse,self).__init__(parent)
		#self.eventType = "windows_generic_MSG"
		self.Mainpointer = self
		self.WindowChildren = []
		self.Main_x = 0
		self.Main_y = 0
		self.MainSize_x = 0
		self.MainSize_y = 0
		self.Frequency = 200
		self._Ch_num = 20
		self._playtime = 0
		self._TimeScale = 10
		self._LoadingPivot = 0
		self.btn_click = False
		self.update = False
		self.preload = False
		self.remove = False
<<<<<<< HEAD
		self.manager = manager
=======
		self.jump = False
>>>>>>> ThreadDone
		self.initUI()


		self.existfft=0
 	

	@property
	def Ch_num(self):
		return self._Ch_num
	@property
	def playtime(self):
		return self._playtime
	@property
	def TimeScale(self):
		return self._TimeScale
	@property
	def LoadingPivot(self):
		return self._LoadingPivot
	

	@TimeScale.setter
	def TimeScale(self,value):
		if value < 0.1:
			self._TimeScale = 0.1
		elif value > 600:
			self._TimeScale = 600
		else:
			self._TimeScale = value
			self.TimeScaleChanged.emit()

	@playtime.setter
	def playtime(self,value):
		if value < 0 :
			self._playtime = 0
		else:
			if abs(value - self._playtime) > self._TimeScale:
				self.jump = True
			self._playtime = value
			self.playtimeChanged.emit()

	@Ch_num.setter
	def Ch_num(self,value):
		self._Ch_num = value

		self.Ch_numChanged.emit()

	@LoadingPivot.setter
	def LoadingPivot(self,value):
		self._LoadingPivot = value


	


	def initUI(self):
		openAction = QAction('Open',self)
		openAction.setShortcut('Ctrl+O')
		self.OpenFile = types.MethodType(Menuaction.OpenFile,self)
		openAction.triggered.connect(self.OpenFile)

		STFTAction = QAction('Powerspectrum',self)
		STFTAction.setShortcut('Alt+P')
		self.STFT = types.MethodType(Menuaction.STFT,self)
		STFTAction.triggered.connect(self.STFT)
		

		# 메인 윈도우 메뉴바
		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openAction)
		fileMenu = menubar.addMenu('&Tools')
		fileMenu.addAction(STFTAction)
		#self.setWindowFlags(Qt.CustomizeWindowHint)
		self.setWindowTitle('EDFbrowser')
		self.screen = QDesktopWidget().availableGeometry()
		self.resize(self.screen.width(),self.screen.height())
		self.MainSize_x = self.size().width()
		self.MainSize_y = self.size().height()

		
		self.resize(self.screen.width(),self.screen.height())
		self.showMaximized()
				
		#self.SignalWindow.setWindowFlags(Qt.FramelessWindowHint)

	def nativeEvent(self,eventType,message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if eventType == "windows_generic_MSG":
			if msg.message == win32con.WM_NCLBUTTONDOWN:
				nHittest = int(msg.wParam)
				if nHittest in [win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
					self.WindowChildren = []



					for child in self.findChildren(QWidget):
						if 'frame' in str(child).lower():
							self.WindowChildren.append(child)
							child.setChildWidgetInfo()
					
					if not nHittest == win32con.HTCAPTION:
						
						self.MainSize_x = self.size().width()
						self.MainSize_y = self.size().height()
						for childframe in self.WindowChildren:
							childframe.setChildWidgetInfo()

					self.WindowChildren_baseSize = []
					for WindowChild in self.WindowChildren:
						self.WindowChildren_baseSize.append([WindowChild.size().width(),WindowChild.size().height(),WindowChild.geometry().x(),WindowChild.geometry().y()])
					

		return False, 0
	
	"""
	def moveEvent(self,e):
		move_x = e.pos().x() - self.Main_x
		move_y = e.pos().y() - self.Main_y

		for WindowChild in self.WindowChildren:
			WindowChild.move(WindowChild.pos().x() + move_x, WindowChild.pos().y() + move_y)

		self.Main_x = e.pos().x()
		self.Main_y = e.pos().y()
	
	"""

	def resizeEvent(self,e):
		xSizeChangeRatio = (1+(e.size().width() - self.MainSize_x ) / self.MainSize_x)
		ySizeChangeRatio = (1+(e.size().height() - self.MainSize_y )/ self.MainSize_y)
		i=0
		for WindowChild in self.WindowChildren:
			WindowChild.setGeometry(int(self.WindowChildren_baseSize[i][2]*xSizeChangeRatio),
									int(self.WindowChildren_baseSize[i][3]*ySizeChangeRatio),
									self.WindowChildren_baseSize[i][0]*xSizeChangeRatio,
									self.WindowChildren_baseSize[i][1]*ySizeChangeRatio)
			i=i+1

	
	def on_playtimeChanged(self):
		self.SignalFrame.PlayTimeUpdated()
<<<<<<< HEAD


	#def on_TimeScaleChanged(self):

class DataManage(object):
	def __init__(self):
		self.ck_load = 0
		self.plotdata = 0
		self.unit = 0
		self.chanel_num = 0
		self.run = True
		self.playtime = 0
		self.timescale = 60
		self.duration = 0
		self.Frequency = 0
class MyManager(BaseManager): pass

class ProxyBase(NamespaceProxy):
	_exposed_ = ('__getattribute__', '__setattr__', '__delattr__')

class DataManageProxy(ProxyBase): pass
class edfProxy(ProxyBase): pass


def register_proxy(name, cls, proxy):
	for attr in dir(cls):
		if inspect.ismethod(getattr(cls, attr)) and not attr.startswith("__"):
			proxy._exposed_ += (attr,)
			setattr(proxy, attr, 
			lambda s: object.__getattribute__(s, '_callmethod')(attr))
	MyManager.register(name, cls, proxy)

register_proxy('DataManage', DataManage,DataManageProxy)
register_proxy('EdfReader', pyedflib.EdfReader,edfProxy)
=======
		
		#pt = self.showfft.getPlaytimeChanged(self.playtime)
		#showfft.show_fft(self,ptdata)
		if self.existfft == 1:
			showfft.getplaytimechanged(self)
	def on_TimeScaleChanged(self):
		#ts = self.showfft.getTimescaleChanged(self.timescale)
		if self.existfft == 1:
			showfft.gettimescalechanged(self)
>>>>>>> master


if __name__ == '__main__':
   app = QApplication(sys.argv)
   m = MyManager()
   m.start()
   datam = m.DataManage()
   ex = EDFbrowse(datam)
   ex.playtimeChanged.connect(ex.on_playtimeChanged)
<<<<<<< HEAD
   
=======
   ex.TimeScaleChanged.connect(ex.on_TimeScaleChanged)
>>>>>>> master
   sys.exit(app.exec_())