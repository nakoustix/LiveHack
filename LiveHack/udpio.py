from _io import StringIO
import socket

class UDPOut(StringIO):
	def __init__(self, address, port):
		super(UDPOut, self).__init__("", "\n")
		self.address = address
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
	def write(self, s):
		self.socket.sendto(bytes(s, "utf-8"), (self.address, self.port))
		
			
	def close(self):
		self.socket.close()
		