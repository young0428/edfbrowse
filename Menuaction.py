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

def OpenFile(self):
	fname = QFileDialog.getOpenFileName(self, 'Open file', './')
	if fname[0] :
		if not fname[0][len(fname[0])-4:] == '.edf':
			sys.stderr.write("Failed to Open")
			sys.exit(1)

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
def OpenDet(self):
	fname = QFileDialog.getOpenFileName(self, 'Open file', './')
	if fname[0] :
		if not fname[0][len(fname[0])-4:] == '.csv':
			sys.stderr.write("Failed to Open")

def OpenPred(self):
	pass

	
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


