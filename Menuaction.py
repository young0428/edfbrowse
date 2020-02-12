import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyedflib
import MakeWindow
import time


def OpenFile(self):
	fname = QFileDialog.getOpenFileName(self, 'Open file', './')
	if fname[0] :
		if not fname[0][len(fname[0])-4:] == '.edf':
			sys.stderr.write("Failed to Open")
			sys.exit(1)


	edf = pyedflib.EdfReader(fname[0])
	self.EDF = edf
	self.FullCh_num = self.EDF.signals_in_file
	self.Frequency = self.EDF.getSampleFrequency(0)
	self.duration = self.EDF.datarecord_duration
	self.manager.frequency = int(self.Frequency)
	self.manager.duration = float(self.EDF.datarecord_duration)
	self.manager.ck_load = [0]*int(edf.datarecords_in_file)
	self.manager.plotdata = [[None]*self.FullCh_num]*edf.datarecords_in_file
	self.manager.unit = 1/self.Frequency


	
	
	MakeWindow.mkChannelSelect(self)
	


def STFT(self):
	class STFTWindow(QWidget):
		def __init__(self,parent):
			super(STFTWindow,self).__init__(parent)
			self.lbl = QLabel('This is STFT',self)
			self.lbl.setStyleSheet("color : red; border-style:solid; border-width: 10px; border-color:#FA8072; border-radius: 3px;background-color:#FFFFFF")
			self.lbl.move(0,50)
			self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
			#
	
	self.STFTwindow = STFTWindow(self)
	self.STFTwindow.resize(400,200)
	STFT_width = self.STFTwindow.frameGeometry().width()
	self.STFTwindow.lbl.resize(STFT_width,40)
	self.STFTwindow.setWindowTitle('STFT')
	self.STFTwindow.show()
