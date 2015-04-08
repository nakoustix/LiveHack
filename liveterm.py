import sys
from io import StringIO
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot
from console import Console
import socket

class MainWindow(QMainWindow):
    
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		#icon = QIcon("logo.png")
		#self.setWindowIcon(icon)
		self.setWindowTitle("LiveHack by nAkoustix v0.1")
		
		self.console = Console(self)
		self.lay = QGridLayout()
		self.lay.addWidget(self.console, 0,0)
        
		cw = QWidget(self)
		cw.setLayout(self.lay)
		self.setCentralWidget(cw)
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.setblocking(0)
		self.localAddr = ("localhost", 9001)
		self.socket.bind(self.localAddr)
		
		self.socksend = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.remoteAddr = ("localhost", 9000)
		
		self.buffer = []
		self.indentation = 0
		
		self.readTimer = QTimer(self)
		self.readTimer.timeout.connect(self.readData)
		
		self.console.newLine.connect(self.interpretLine)
		
		self.readTimer.start(50)
		
		self.console.makePrompt()
		
	def interpretLine(self, line):
		if line[:3] != ">>>" and line[:3] != "...":
			self.console.putData("\n")
			self.console.makePrompt()
			return
		line = line[4:]
		self.buffer += [line]
		self.console.addToCmdHistory(line)
		if line[-1:] == ":":
			self.console.putData("\n")
			self.indentation += 1
			self.console.makeExtendedPrompt(self.indentation)
		else:
			self.console.putData("\n")
			if self.indentation == 0:
				self.execute()
				self.console.makePrompt()
			else:
				self.indentation = 0
				self.console.makeExtendedPrompt(self.indentation)
				
	def execute(self):
		s = ""
		for line in self.buffer:
			s += line + "\n"
		# check if there is anything
		if len(self.buffer) == 1 and self.buffer[0] == "":
			pass
		else:
			#print(s)
			self.socksend.sendto(bytes(s, "utf-8"), self.remoteAddr)
			self.socksend.sendto("execute".encode("utf-8"), self.remoteAddr)
		self.buffer = []
		
	def readData(self):
		try:
			while 1:
				self.data, self.addr = self.socket.recvfrom(65536)
				decoded = self.data.decode()
				#print(decoded)
				if decoded != "" and decoded != "\n":
					self.console.putData("\n")
					self.console.putData(decoded)

		except Exception as e:
			pass
   
        
def main():
    
	app = QApplication(sys.argv)
	geom = app.desktop().geometry()
    
	w = MainWindow()
    #w.resize(1000, 900)
    
	w.setGeometry(700,300,800,500)
	w.show()
    
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()