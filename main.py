import sys
import types
import ctypes
import math
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

import Menuaction
import MakeWindow
import show_fft_function as showfft
import timelinetest as dp

class EDFbrowse(QMainWindow):

	TimeScaleChanged = pyqtSignal()
	Ch_numChanged = pyqtSignal()
	playtimeChanged = pyqtSignal()
	ctrl_release = pyqtSignal()

	def __init__(self,parent=None):
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
		self.line_per_time = 1
		self.btn_click = False
		self.update = False
		self.preload = False
		self.remove = False
		self.jump = False
		self.viewbox_exist = False
		self.max_playtime =6000
		self.ds = 4
		self.existfft=0 
		self.sigexist = False
		self.EDF = None
		self.FFTFrame =None
		self.Selected_Channels_index = None
		self.ChannelOpen = False
		self.initUI()


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
		elif value+self._TimeScale > self.max_playtime:
			self._playtime = self.max_playtime-self._TimeScale
		else:
			if abs(value - self._playtime) > self._TimeScale*2:
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

		#self.setStyleSheet('background:#333333;')
		openAction = QAction('Open EDF',self)
		openAction.setShortcut('Ctrl+O')
		self.OpenFile = types.MethodType(Menuaction.OpenFile,self)
		openAction.triggered.connect(self.OpenFile)

		closeAction = QAction('Close EDF',self)
		self.CloseFile = types.MethodType(Menuaction.CloseFile,self)
		closeAction.triggered.connect(self.CloseFile)

		openAnalAction = QAction('Open Analysis',self)
		openAnalAction.setShortcut('Ctrl+A')
		self.OpenDp = types.MethodType(Menuaction.OpenDp,self)
		openAnalAction.triggered.connect(self.OpenDp)

		STFTAction = QAction('Powerspectrum',self)
		STFTAction.setShortcut('Alt+P')
		self.STFT = types.MethodType(Menuaction.STFT,self)
		STFTAction.triggered.connect(self.STFT)

		memoAction = QAction('Memo',self)
		memoAction.setShortcut('Alt+M')
		self.memo = types.MethodType(Menuaction.memo,self)
		memoAction.triggered.connect(self.memo)

		saveAction = QAction('Save',self)
		saveAction.setShortcut('Ctrl+S')
		self.save = types.MethodType(Menuaction.save,self)
		saveAction.triggered.connect(self.save)


		# 메인 윈도우 메뉴바
		self.menubar = self.menuBar()
		self.menubar.setNativeMenuBar(False)
		fileMenu = self.menubar.addMenu('&File')
		fileMenu.addAction(openAction)
		fileMenu.addAction(closeAction)
		fileMenu.addAction(openAnalAction)
		fileMenu.addAction(saveAction)
		fileMenu = self.menubar.addMenu('&Tools')
		fileMenu.addAction(STFTAction)
		fileMenu.addAction(memoAction)

		#self.setWindowFlags(Qt.CustomizeWindowHint)
		self.setWindowTitle('EDFbrowser')
		self.screen = QDesktopWidget().availableGeometry()
		self.resize(self.screen.width(),self.screen.height())
		self.MainSize_x = self.size().width()
		self.MainSize_y = self.size().height()

		#self.setGeometry(self.MainSize_x//4,self.MainSize_y//4,self.MainSize_x//2,self.MainSize_y//2)
		self.showMaximized()
		#memotable.mkbtn(self)

				
		#self.SignalWindow.setWindowFlags(Qt.FramelessWindowHint)

	def nativeEvent(self,eventType,message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if eventType == "windows_generic_MSG":
			if msg.message == win32con.WM_NCLBUTTONDOWN:
				nHittest = int(msg.wParam)
				if nHittest in [win32con.HTMAXBUTTON,win32con.HTMINBUTTON,win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
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
			
			elif msg.message == win32con.WM_NCLBUTTONDBLCLK:
				for child in self.findChildren(QWidget):
					if 'frame' in str(child).lower():
						self.WindowChildren.append(child)
						child.setChildWidgetInfo()
					
				self.MainSize_x = self.size().width()
				self.MainSize_y = self.size().height()
				for childframe in self.WindowChildren:
					childframe.setChildWidgetInfo()


				self.WindowChildren_baseSize = []
				for WindowChild in self.WindowChildren:
					self.WindowChildren_baseSize.append([WindowChild.size().width(),WindowChild.size().height(),WindowChild.geometry().x(),WindowChild.geometry().y()])

			if msg.message == win32con.WM_KEYDOWN:
				nHittest = int(msg.wParam)
				if self.viewbox_exist:
					if nHittest == win32con.VK_CONTROL:
						self.SignalFrame.PlotViewBox.CtrlPress = True
						self.DPFrame.detviewbox.CtrlPress = True
						self.DPFrame.predviewbox.CtrlPress = True
					if nHittest == win32con.VK_RIGHT:
						if self.SignalFrame.PlotViewBox.CtrlPress:
							self.btn_click = True
							self.playtime += self.TimeScale
							self.btn_click = False
						else:
							self.btn_click = True
							self.playtime += 1
							self.btn_click = False
					if nHittest == win32con.VK_LEFT:
						if self.SignalFrame.PlotViewBox.CtrlPress:
							self.btn_click = True
							self.playtime -= self.TimeScale
							self.btn_click = False
						else:
							self.btn_click = True
							self.playtime -= 1
							self.btn_click = False
				



			if msg.message == win32con.WM_KEYUP:
				nHittest = int(msg.wParam)
				if self.viewbox_exist:
					if nHittest == win32con.VK_CONTROL:
						self.SignalFrame.PlotViewBox.CtrlPress = False
						self.DPFrame.detviewbox.CtrlPress = False
						self.DPFrame.predviewbox.CtrlPress = False
						if self.SignalFrame.dragging:
							self.SignalFrame.UpdatePlotting.StartUpdate(0)
							self.SignalFrame.UpdatePlotting.StartUpdate(1)
							self.SignalFrame.dragging = False
						
						self.ctrl_release.emit()
					
					

		return False, 0

	
	def resizeEvent(self,e):
		xSizeChangeRatio = (1+(e.size().width() - self.MainSize_x ) / self.MainSize_x)
		ySizeChangeRatio = (1+(e.size().height() - self.MainSize_y )/ self.MainSize_y)
		i=0
		for WindowChild in self.WindowChildren:
			if WindowChild == self.SignalFrame:
				WindowChild.setGeometry((self.WindowChildren_baseSize[i][2]*xSizeChangeRatio),
									(self.WindowChildren_baseSize[i][3]*ySizeChangeRatio+math.ceil(self.menubar.height()*(1-ySizeChangeRatio))),
									math.ceil(self.WindowChildren_baseSize[i][0]*xSizeChangeRatio),
									math.ceil(self.WindowChildren_baseSize[i][1]*ySizeChangeRatio)-math.ceil(self.menubar.height()*(1-ySizeChangeRatio)))
			elif WindowChild == self.FFTFrame:
				pass
			else:
				WindowChild.setGeometry((self.WindowChildren_baseSize[i][2]*xSizeChangeRatio),
									(self.WindowChildren_baseSize[i][3]*ySizeChangeRatio),
									math.ceil(self.WindowChildren_baseSize[i][0]*xSizeChangeRatio),
									math.ceil(self.WindowChildren_baseSize[i][1]*ySizeChangeRatio))
			i=i+1
		xSizeChangeRatio=1
		ySizeChangeRatio=1
	

	def on_playtimeChanged(self):
		self.SignalFrame.PlayTimeUpdated()
		
		#pt = self.showfft.getPlaytimeChanged(self.playtime)
		#showfft.show_fft(self,ptdata)
		if self.existfft == 1:
			showfft.getplaytimechanged(self)
	def on_TimeScaleChanged(self):
		#ts = self.showfft.getTimescaleChanged(self.timescale)
		if self.existfft == 1:
			showfft.gettimescalechanged(self)

	def closeEvent(self,e):
		msgbox=QMessageBox(self)
		ok = msgbox.question(self,'', 'Do you want to quit?', QMessageBox.Yes | QMessageBox.No)
		if ok==QMessageBox.Yes:
			pass
		else:
			e.ignore()
		for child in self.findChildren(QWidget):
			if 'frame' in str(child).lower():
				
				child.close()
				if child.fail_to_close:
					e.ignore()
					break
		if not self.EDF == None:
			self.EDF._close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = EDFbrowse()
	ex.playtimeChanged.connect(ex.on_playtimeChanged)
	ex.TimeScaleChanged.connect(ex.on_TimeScaleChanged)
	sys.exit(app.exec_())
