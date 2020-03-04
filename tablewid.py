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

class MyTable(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		memobox =QWidget(parent)
		memobox.setGeometry(0,0,400,400)
		memoscr = QScrollArea(memobox)
		memoscr.setGeometry(0,0,400,400)
		memotable = QTableWidget(memoscr)
		memotable.setGeometry(0,0,400,400)
		memotable.setColumnCount(5)
		memotable.setRowCount(3)

class MyMain(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(400,400)
		table = MyTable(self)
		self.setCentralWidget(table)
		self.statusbar = self.statusBar()

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	app.setStyle(QStyleFactory.create('Fusion'))
	w = MyMain()
	w.show()
	sys.exit(app.exec())