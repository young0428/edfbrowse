import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyedflib
import MakeWindow
import time
import show_fft_function as showfft

start_xpx = 0
start_ypx = 0
xpx = 1600
ypx = 250
in_xpx = xpx - 2*start_xpx
in_ypx = ypx - 2*start_ypx


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
			self.Main.FFTFrame.setWindowTitle('xxxxx')
			self.Main.FFTFrame.setGeometry(start_xpx,start_ypx,in_xpx,in_ypx)
			showfft.show_fft(self.Main,showfft.make_data(self.Main.FFTFrame,self.Main.EDF))
			self.Main.win.show()
			

		
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


