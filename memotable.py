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
import copy
import math
import os
import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ctypes.wintypes import POINT
from functools import partial

import Menuaction
import timelinetest


class memowin(QWidget):
	CtrlZsignal = pyqtSignal()
	def __init__(self,parent=None):
		super(memowin,self).__init__(parent)
		self.parent = parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint|Qt.Window)
		self.setWindowTitle("Memo")
		self.initResized = False
		self.ctrl_press = False
		self.center()

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	
	def setChildWidgetInfo(self):
		self.ChildrenWidget = []

		for widget in self.findChildren(QWidget):
			self.ChildrenWidget.append(widget)
	'''
	def nativeEvent(self,eventType,message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if eventType == "windows_generic_MSG":
			if msg.message == win32con.WM_NCLBUTTONDOWN:
				nHittest = int(msg.wParam)
				if nHittest in [win32con.HTCAPTION,win32con.HTBOTTOM,win32con.HTBOTTOMLEFT,win32con.HTBOTTOMRIGHT,win32con.HTLEFT,win32con.HTRIGHT,win32con.HTTOP,win32con.HTTOPLEFT,win32con.HTTOPRIGHT]:
					self.setChildWidgetInfo()
		return False, 0
	
	'''
	def nativeEvent(self,eventType,message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if eventType == "windows_generic_MSG":
			if msg.message == win32con.WM_KEYDOWN:
				nHittest = int(msg.wParam)
				if nHittest == win32con.VK_CONTROL:
					self.ctrl_press = True
				if nHittest == 90 and self.ctrl_press:
					self.CtrlZsignal.emit()
			if msg.message == win32con.WM_KEYUP:
				nHittest = int(msg.wParam)
				if nHittest == win32con.VK_CONTROL:
					self.ctrl_press = False
						
				
					
					

		return False, 0
	def resizeEvent(self,e):
		if self.initResized:
			for childwidget in self.ChildrenWidget:
				if str(type(childwidget)) == "<class 'PyQt5.QtWidgets.QTableWidget'>" :
					childwidget.setColumnWidth(2,childwidget.geometry().width()-220-childwidget.verticalHeader().width())
					childwidget.updateGeometry()


		else:
			self.setChildWidgetInfo()
			self.initResized = True

def mkmemotable(self): #self == frame
	if 	self.parent.EDF != None:
		self.parent.memobox = memowin(self.parent)
		memolay =QVBoxLayout(self.parent.memobox)
		self.parent.memobox.setLayout(memolay)
		self.parent.memotable = QTableWidget(self.parent.memobox)
		self.parent.memotable.parent = self.parent
		self.parent.memotable.zbox = []
		memolay.addWidget(self.parent.memotable,0)

		headers = ['Start','End','Annotation']
		
		self.parent.edfname = os.path.basename(self.parent.fname[0])
		self.parent.dir = os.path.dirname(self.parent.fname[0])
		self.parent.csvpath = self.parent.dir+'/memo'+self.parent.edfname[:-4]+'.csv'
		if os.path.exists(self.parent.csvpath):
			data = pd.read_csv(self.parent.csvpath,error_bad_lines=False,encoding="euc-kr")
			#data = data.where(pd.notnull(data),None)
			annostart = list(data['Start'])
			annoend = list(data['End'])
			anno = list(data['Annotation'])
		else:
			annostart = []
			annoend = []
			anno = []

		self.parent.memotable.setRowCount(len(anno))
		self.parent.memotable.setColumnCount(3)
		self.parent.memotable.setHorizontalHeaderLabels(headers)
		self.parent.memotable.setColumnWidth(0,100)
		self.parent.memotable.setColumnWidth(1,100)
		self.parent.memotable.setColumnWidth(2,400)
		self.parent.memobox.setMinimumWidth(620+self.parent.memotable.verticalHeader().width()+self.parent.memotable.verticalHeader().x())
		self.parent.memotable.setColumnWidth(2,self.parent.memotable.geometry().width()-220-self.parent.memotable.verticalHeader().width())
		self.parent.memotable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.parent.memotable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		self.parent.memotable.setCornerButtonEnabled(False)
		def changed(self,row=0,col=0):
			inst_list = []
			for row in range(self.rowCount()):
				L = []
				for col in range(self.columnCount()):
					if self.cellWidget(row,col) == None:
						return None
					else:
						L.append(self.cellWidget(row,col).text())
				inst_list.append(L)

			if len(self.zbox) > self.zbox_cnt:
				self.zbox = self.zbox[:self.zbox_cnt]
			self.zbox.append(inst_list)
			self.zbox_cnt += 1
		self.parent.memotable.changed = partial(changed,self.parent.memotable)


		for row in range(len(anno)):
			a = QLineEdit(str(annostart[row]))
			a.setInputMask('00:00:00.00')
			a.editingFinished.connect(self.parent.memotable.changed)
			a.returnPressed.connect(self.parent.memotable.changed)
			self.parent.memotable.setCellWidget(row,0,a)
			a = QLineEdit(str(annoend[row]))
			a.setInputMask('00:00:00.00')
			a.editingFinished.connect(self.parent.memotable.changed)
			a.returnPressed.connect(self.parent.memotable.changed)
			self.parent.memotable.setCellWidget(row,1,a)
			if str(anno[row]) == 'nan':
				a = QLineEdit()
			else:
				a = QLineEdit(str(anno[row]))
			a.editingFinished.connect(self.parent.memotable.changed)
			a.returnPressed.connect(self.parent.memotable.changed)	
			self.parent.memotable.setCellWidget(row,2,a)


					
			
		

		self.zbox = []

		self.parent.btnlay = QHBoxLayout()
		memolay.addLayout(self.parent.btnlay,1)
		btnlist(self)
		btnfunc(self)

		
		"""
		inst_list = []
		for row in range(self.parent.memotable.rowCount()):
			L = []
			for col in range(self.parent.memotable.columnCount()):
				L.append(self.parent.memotable.cellWidget(row,col).text())
			inst_list.append(L)
		self.parent.memotable.zbox.append(inst_list)
		self.parent.memotable.zbox_cnt = 1
		"""
		self.parent.memotable.zbox_cnt = 0
				

def btnlist(self):
	#line 추가, 제거
	self.parent.adlay = QHBoxLayout()
	self.parent.addbtn = QPushButton('Add')
	self.parent.addbtn.setFixedWidth(self.parent.memobox.width()//8)
	self.parent.delbtn = QPushButton('Delete')
	self.parent.delbtn.setFixedWidth(self.parent.memobox.width()//8)

	self.parent.adlay.addWidget(self.parent.addbtn)
	self.parent.adlay.addWidget(self.parent.delbtn)
	self.parent.adlay.setSizeConstraint(QLayout.SetMinimumSize)
	self.parent.adlay.setAlignment(Qt.AlignLeft)

	#저장 취소
	self.parent.sclay = QHBoxLayout()
	self.parent.savebtn = QPushButton('Save')
	self.parent.savebtn.setFixedWidth(self.parent.memobox.width()//8)
	self.parent.closebtn = QPushButton('Close')
	self.parent.closebtn.setFixedWidth(self.parent.memobox.width()//8)

	self.parent.sclay.addWidget(self.parent.savebtn)
	self.parent.sclay.addWidget(self.parent.closebtn)
	self.parent.sclay.setSizeConstraint(QLayout.SetMinimumSize)
	self.parent.sclay.setAlignment(Qt.AlignRight)

	self.parent.btnlay.addLayout(self.parent.adlay)
	self.parent.btnlay.addLayout(self.parent.sclay)

def btnfunc(self):
	

	def addF(self,start=None,end=None,anno=None):
		row_count = self.parent.memotable.rowCount()
		self.parent.memotable.setRowCount(row_count+1)

		if type(start) == type(True):
			start = None

		if start == None:
			start = '00000000'
		if end == None:
			end = '00000000'

		start.replace(':','')
		start.replace('.','')
		end.replace(':','')
		end.replace('.','')

		if start > end:
			temp = start
			start = end
			end = temp

		a = QLineEdit(start)
		a.editingFinished.connect(self.parent.memotable.changed)
		a.returnPressed.connect(self.parent.memotable.changed)
		a.setInputMask('00:00:00.00')
		self.parent.memotable.setCellWidget(row_count,0,a)

		a = QLineEdit(end)
		a.editingFinished.connect(self.parent.memotable.changed)
		a.returnPressed.connect(self.parent.memotable.changed)
		a.setInputMask('00:00:00.00')
		self.parent.memotable.setCellWidget(row_count,1,a)

		a = QLineEdit()
		a.editingFinished.connect(self.parent.memotable.changed)
		a.returnPressed.connect(self.parent.memotable.changed)
		self.parent.memotable.setCellWidget(row_count,2,a)

		self.parent.memotable.changed(0,0)


	def delF(frame):
		removeidx = []
		cnt=0
		ranges = self.parent.memotable.selectedRanges()
		for idx in ranges:
			for ro in range(idx.rowCount()):
				if idx.topRow()+ro in removeidx:
					pass
				else:
					removeidx.append(idx.topRow()+ro)
		removeidx.sort()
		for i in removeidx:
			self.parent.memotable.removeRow(i-cnt)
			cnt = cnt + 1

		self.parent.memotable.changed(0,0)


	def saveF(frame):
		#self.parent.memotable
		inst_list =  []
		headers = ['Start','End','Annotation']
		for row in range(self.parent.memotable.rowCount()):
			L = []
			for col in range(self.parent.memotable.columnCount()):
				if not self.parent.memotable.cellWidget(row,col) is None:
					L.append(self.parent.memotable.cellWidget(row,col).text())
				else:
					L.append(None)

			inst_list.append(L)

		df = pd.DataFrame(inst_list,columns=headers)
		try:
			df.to_csv('./anno/'+'memo'+self.parent.edfname[:-4]+'_save'+'.csv',mode='w',index=False,encoding="euc-kr")
			df.to_csv(self.parent.dir+'/memo'+self.parent.edfname[:-4]+'.csv',mode='w',index=False,encoding="euc-kr")
		except:
			emsg = QMessageBox().critical(self,'Save Error','Save Error : Annotation File is open.')
			return -1

	

	def ctrlz(self):
		if self.parent.memotable.zbox_cnt == 1:
			pass
		else:
			table = self.parent.memotable.zbox[self.parent.memotable.zbox_cnt-2]
			self.parent.memotable.setRowCount(0)
			self.parent.memotable.setRowCount(len(table))
			for row in range(len(table)):
				a = QLineEdit(table[row][0])
				a.editingFinished.connect(self.parent.memotable.changed)
				a.returnPressed.connect(self.parent.memotable.changed)
				a.setInputMask('00:00:00.00')
				self.parent.memotable.setCellWidget(row,0,a)
				a = QLineEdit(table[row][1])
				a.editingFinished.connect(self.parent.memotable.changed)
				a.returnPressed.connect(self.parent.memotable.changed)
				a.setInputMask('00:00:00.00')
				self.parent.memotable.setCellWidget(row,1,a)
				a = QLineEdit(table[row][2])
				a.editingFinished.connect(self.parent.memotable.changed)
				a.returnPressed.connect(self.parent.memotable.changed)
				self.parent.memotable.setCellWidget(row,2,a)

			self.parent.memotable.zbox_cnt -= 1


	def closeF(frame):
		self.parent.memobox.close()

	
	self.addF = partial(addF,self)
	self.delF = partial(delF,self)
	self.saveF = partial(saveF,self)
	self.closeF = partial(closeF,self)
	self.ctrlz = partial(ctrlz,self)

	self.parent.memobox.CtrlZsignal.connect(self.ctrlz)


	self.parent.memotable.cellChanged.connect(self.parent.memotable.changed)	
	self.parent.addbtn.clicked.connect(self.addF)
	self.parent.delbtn.clicked.connect(self.delF)
	self.parent.savebtn.clicked.connect(self.saveF)
	self.parent.closebtn.clicked.connect(self.closeF)


