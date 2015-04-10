import sys
from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QByteArray
from PyQt5.QtGui import QPalette, QFontMetrics

class Console(QPlainTextEdit):
	newLine = pyqtSignal(str)
	indentationPlus = pyqtSignal()
	indentationMinus = pyqtSignal()
	#suppressedKeys = [Qt.Key_Backspace, Qt.Key_Left, Qt.Key_Right, Qt.Key_Up,
		#			Qt.Key_Down]
	suppressedKeys = []
	specialKeys = [Qt.Key_Backspace, Qt.Key_Return, Qt.Key_Left, Qt.Key_Up, Qt.Key_Down, 
				Qt.Key_Tab, Qt.Key_Space]
					
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
		self.cmdHistory = []
		self.cmdHistoryPos = 0
		self.spaceCount = 0
		
	def putData(self, data):
		self.insertPlainText(str(data))
		bar = self.verticalScrollBar()
		bar.setValue(bar.maximum())
		
	def makePrompt(self):
		self.putData(">>> ")
		
	def makeExtendedPrompt(self, indent):
		self.putData("... ")
		for i in range(indent * 4):
			self.putData(" ")
		
	def isPromptLine(self, line): 
		return line[:3] == ">>>" or line[:3] == "..."
		
	def keyPressEvent(self, e):
		key = e.key()
		if key in self.suppressedKeys:
			return
		if key in self.specialKeys:
			if key == Qt.Key_Return:
				cline = self.textCursor().block().text()
				self.newLine.emit(cline)
			elif key == Qt.Key_Backspace:
				cline = self.textCursor().block().text() 
				rect = self.cursorRect()
				cPos = int(rect.x() / self.charWidth)
				if self.isPromptLine(cline) and cPos > 4:
					super(Console, self).keyPressEvent(e)
			elif key == Qt.Key_Tab:
				self.indentationPlus.emit()
				self.putData("    ")
			elif key == Qt.Key_Left:
				cline = self.textCursor().block().text()
				rect = self.cursorRect()
				cPos = int(rect.x() / self.charWidth)
				if self.isPromptLine(cline) and cPos > 4: 
					super(Console, self).keyPressEvent(e)
			elif key == Qt.Key_Up:
				if len(self.cmdHistory) == 0:
					return
				cmd = self.cmdHistory[self.cmdHistoryPos]
				self.lastHistoryCmdLen = len(cmd)
				self.putData(self.cmdHistory[self.cmdHistoryPos])
				self.cmdHistoryPos -= 1
				if self.cmdHistoryPos < 0:
					self.cmdHistoryPos = 0
			if key == Qt.Key_Space:
				super(Console, self).keyPressEvent(e)
				self.spaceCount += 1
				if self.spaceCount >= 4:
					self.spaceCount = 0
					self.indentationPlus.emit()
			else:
				self.spaceCount = 0
		else:
			super(Console, self).keyPressEvent(e)
			
	def addToCmdHistory(self, cmd):
		self.cmdHistory += [cmd]