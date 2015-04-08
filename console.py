import sys
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QByteArray
from PyQt5.QtGui import QPalette, QFontMetrics

class Console(QPlainTextEdit):
	getData = pyqtSignal(QByteArray)
	#suppressedKeys = [Qt.Key_Backspace, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up,
		#			Qt.Key_Down]
	suppressedKeys = [Qt.Key_Up, Qt.Key_Down]
	specialKeys = [Qt.Key_Backspace, Qt.Key_Return]
					
	def __init__(self, parent = None):
		super(Console, self).__init__(parent)
		pal = self.palette()
		pal.setColor(QPalette.Base, Qt.black)
		pal.setColor(QPalette.Text, Qt.green)
		self.setPalette(pal)
		doc = self.document()
		font = doc.defaultFont()
		font.setFamily("Courier New")
		self.fm = QFontMetrics(font)
		#print(self.fm.width("a"))
		self.charWidth = self.fm.width("a")
		font.setPixelSize(12)
		doc.setDefaultFont(font)
		
	def putData(self, data):
		self.insertPlainText(str(data))
		bar = self.verticalScrollBar()
		bar.setValue(bar.maximum())
		
	def makePrompt(self):
		self.putData(">>> ")

	def keyPressEvent(self, e):
		key = e.key()
		if key in self.suppressedKeys:
			return
		if key in self.specialKeys:
			if key == Qt.Key_Return:
				pass
			elif key == Qt.Key_Backspace:
				rect = self.cursorRect()
				promptLen = int(rect.x() / self.charWidth)
				if promptLen > 4:
					super(Console, self).keyPressEvent(e)
				
		else:
			super(Console, self).keyPressEvent(e)
			self.getData.emit(e.text())