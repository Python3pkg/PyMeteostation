import sys, time
from socket import *

class Broadcaster:
	def __init__(self,ip="<broadcast>", port=50000):
		self.ip = ip
		self.port = port
		self.s = socket(AF_INET, SOCK_DGRAM)
		self.s.bind(('', 0))
		self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	def send(self,data):
	 	self.s.sendto(data, (self.ip, self.port))