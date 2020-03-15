#-*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyedflib
import MakeWindow
import time
import show_fft_function as showfft
import pandas as pd
import numpy as np
import timelinetest as dp

start_xpx = 20
start_ypx = 20
xpx = 1600
ypx = 250

def isKoreanIncluded(word):
	for i in word:
		if ord(i) > int('0x1100',16) and ord(i) < int('0x11ff',16) :
			return True
		if ord(i) > int('0x3131',16) and ord(i) < int('0x318e',16) :
			return True
		if ord(i) > int('0xa960',16) and ord(i) < int('0xa97c',16) :
			return True
		if ord(i) > int('0xac00',16) and ord(i) < int('0xd7a3',16) :
			return True
		if ord(i) > int('0xd7b0',16) and ord(i) < int('0xd7fb',16) :
			return True
	return False

def OpenFile(self):
	fname = QFileDialog.getOpenFileName(self, 'Open file', './')
<<<<<<< Updated upstream
	if fname[0] :
=======
	self.fname = fname
	if isKoreanIncluded(fname[0]):
		QMessageBox().critical(self,'File Open Error','File path have to include ONLY English')
		return None
	if fname[0]:
>>>>>>> Stashed changes
		if fname[0][len(fname[0])-4:] == '.edf':
			

			edf = pyedflib.EdfReader(fname[0])

			self.FullCh_num = edf.signals_in_file
			self.Frequency = edf.getSampleFrequency(0)
			self.EDF = edf
			self.duration = edf.datarecord_duration
			self.ck_load = [0]*int(edf.datarecords_in_file)
			self.plots = [[None]*self.FullCh_num]*len(self.ck_load)
			self.unit = 1/self.Frequency


			self.detData = np.zeros(int(self.duration*edf.datarecords_in_file))
			self.predData = np.zeros(int(self.duration*edf.datarecords_in_file))
			dp.makeDataList(self)
			MakeWindow.mkChannelSelect(self)
		else:
			emsg = QMessageBox().critical(self,'File Open Error','Please open .edf file')
			#emsg.setWindowTitle("File Open Error")
			#emsg.setDetailedText("Please open .edf file");

def OpenDet(self):
	fname = QFileDialog.getOpenFileName(self, 'Open file', './')
<<<<<<< Updated upstream
	if fname[0] :
		if not fname[0][len(fname[0])-4:] == '.csv':
			sys.stderr.write("Failed to Open")
=======
	if fname[0]:
		if fname[0][len(fname[0])-4:] != '.csv':
			QMessageBox().critical(self,'File Open Error','Please open other file')
		else:
			self.dpPath = fname[0]
			data = pd.read_csv(fname[0],encoding = 'CP949',error_bad_lines=False)
			detcol = data['det']
			predcol = data['pred']

			i=0
			for col in detcol:
				if i < len(self.detData):
					if str(col) == 'nan': self.detData[i] = 0
					else: self.detData[i] = col
				i=i+1
			self.DPFrame.det.p.setData(self.detx,self.detData)
			
			i=0
			for col in predcol:
				if i<len(self.predData):
					if str(col) == 'nan': self.predData[i] = 0
					else: self.predData[i] = col
				i=i+1
			self.DPFrame.pred.pr.setData(self.predx,-self.predData)

			self.detData_bef = copy.deepcopy(self.detData)
			#self.DPFrame.det.p.setData(self.detx,self.detData)
			detdataplot(self)

			self.predData_bef = copy.deepcopy(self.predData)	
			#self.DPFrame.pred.p.setData(self.predx,self.predData)
			preddataplot(self)


def detdataplot(self):

	before = self.detData[0]
	detregionstart = 0
	items = self.SignalFrame.SignalPlot.allChildItems()
	for item in items:
		if hasattr(item,'this_is_only_det_region'):
			self.SignalFrame.SignalPlot.removeItem(item)

	if before==0:
		region_on = False
	else:
		region_on = True
	i=0
	for now in self.detData:
		if before != now:
			if region_on :
				
				region_on = False
				region = pg.LinearRegionItem()
				region.this_is_only_det_region = 1
				region.setMovable(False)
				region.setRegion((detregionstart*self.Frequency,i*self.Frequency))
				region.setBrush((210,33,26,50))

				region.lines[0].setPen(pg.mkPen((210,33,26,50)))
				region.lines[1].setPen(pg.mkPen((210,33,26,50)))
				self.SignalFrame.SignalPlot.addItem(region)
			else:
				region_on = True
				detregionstart = i
				
				
		before = self.detData[i]
		i=i+1


def preddataplot(self):

	before = self.predData[0]
	predregionstart = 0
	items = self.SignalFrame.SignalPlot.allChildItems()
	for item in items:
		if hasattr(item,'this_is_only_pred_region'):
			self.SignalFrame.SignalPlot.removeItem(item)
	if before==0:
		region_on = False
	else:
		region_on = True
	i=0
	for now in self.predData:

		if before != now:
			if region_on:
				region_on = False
				region = pg.LinearRegionItem()
				region.this_is_only_pred_region = 1
				region.setMovable(False)
				region.setRegion((predregionstart*self.Frequency,i*self.Frequency))
				region.setBrush((32,130,55,50))

				region.lines[0].setPen(pg.mkPen((32,130,55,50)))
				region.lines[1].setPen(pg.mkPen((32,130,55,50)))
				self.SignalFrame.SignalPlot.addItem(region)
			else:
				region_on = True
				predregionstart = i
				
				
		before = self.predData[i]
		i=i+1
>>>>>>> Stashed changes

def OpenPred(self):
	pass

def CloseFile(self):
	for child in self.findChildren(QWidget):
		if 'frame' in str(child).lower():
			child.close()
	if not self.EDF == None:
		self.EDF._close()

	
def STFT(self):
	class selectedChanelWindow(QMainWindow):
		def __init__(self,parent=None):
			super(selectedChanelWindow,self).__init__(parent)
			self.Main = parent
			self.initUI()
		
		def openfft(self):
			self.close()
			self.Main.existfft = 1
			self.Main.signum = self.Main.Selected_Channels_index[self.ListWidget.currentRow()]
			self.Main.FFTFrame = MakeWindow.childframe(self.Main)
			self.Main.FFTFrame.setGeometry(start_xpx,start_ypx,xpx,ypx)
			self.Main.FFTFrame.setWindowFlags(Qt.Window)
			self.Main.FFTFrame.setWindowTitle("FFT "+self.Main.EDF.getLabel(self.Main.signum))

			showfft.show_fft(self.Main.FFTFrame,showfft.make_data(self.Main,self.Main.EDF))
			self.Main.FFTFrame.show()
			
<<<<<<< Updated upstream

		
		def Cancel(self):
			self.close()

		def initUI(self):
			widget = QWidget()
			vbox = QVBoxLayout()
			hbox = QHBoxLayout()
			self.ListWidget = QListWidget()
			self.ListWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
			for index in self.Main.Selected_Channels_index:
				item = self.ListWidget.addItem(self.Main.EDF.getLabel(index))

			self.ListWidget.selectAll()

			OKButton = QPushButton('OK')
			CancelButton = QPushButton('Cancel')
			OKButton.clicked.connect(self.openfft)
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

	a = selectedChanelWindow(self)
		
	"""
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
	"""
		

	class STFTWindow(QWidget):
		def __init__(self,parent):
			super(STFTWindow,self).__init__(parent)
			#self.lbl = QLabel('This is STFT',self)
			#self.lbl.setStyleSheet("color : red; border-style:solid; border-width: 10px; border-color:#FA8072; border-radius: 3px;background-color:#FFFFFF")
			#self.lbl.move(0,50)
			#self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
			#


	self.STFTwindow = STFTWindow(self)
	#self.STFTwindow.resize(400,200)
	#STFT_width = self.STFTwindow.frameGeometry().width()
	#self.STFTwindow.lbl.resize(STFT_width,40)
	#self.STFTwindow.setWindowTitle('STFT')
	#self.STFTwindow.show()


=======
			def openfft(self):
				self.close()
				if self.Main.existfft==1:
					self.Main.FFTFrame.close()
				self.Main.existfft = 1
				self.Main.signum = self.Main.Selected_Channels_index[self.ListWidget.currentRow()]
				self.Main.FFTFrame = MakeWindow.fftframe(self.Main)
				self.Main.FFTFrame.parent=self.Main
				self.Main.FFTFrame.setGeometry(start_xpx,start_ypx,xpx,ypx)
				self.Main.FFTFrame.setWindowFlags(Qt.Window)
				self.Main.FFTFrame.setWindowTitle("[ FFT ] "+self.Main.EDF.getLabel(self.Main.signum))

				showfft.show_fft(self.Main.FFTFrame,showfft.make_data(self.Main,self.Main.EDF))
				self.Main.FFTFrame.show()
				
			def Cancel(self):
				self.close()

			def initUI(self):
				widget = QWidget()
				vbox = QVBoxLayout()
				hbox = QHBoxLayout()
				self.ListWidget = QListWidget()
				for index in self.Main.Selected_Channels_index:
					item = self.ListWidget.addItem(self.Main.EDF.getLabel(index))

				OKButton = QPushButton('OK')
				CancelButton = QPushButton('Cancel')
				OKButton.clicked.connect(self.openfft)
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



		a = selectedChanelWindow(self)

def memo(main):
	if main.EDF != None:
		main.memobox.show()


def save(main):
	if main.sigexist:
		main.SignalFrame.saveF()
		headers = ['det','pred']
		df = pd.DataFrame(list(zip(main.detData,main.predData)),columns=headers)
		if hasattr(main,'dpPath'):
			df.to_csv(main.dpPath,mode='w',index=False)
		else:
			df.to_csv('./detpred/'+'dp_'+self.parent.edfname[:-4]+'_save'+'.csv',mode='w',index=False)
>>>>>>> Stashed changes
