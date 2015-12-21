#Final Project Program Jaringan Kelas D 2015
#Author : Guruh, Burhan, Ghulam, Hanif

import socket 

class Client:
	def __init__(self,(ip,port)):
		self.serverip 	= ip
		self.port 		= port
		self.server 	= None

	def opensocket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect((self.ip,self.port))
		welcome_msg = self.server.recv(1024)
		print welcome_msg
	
	def run(self):
		self.opensocket()
		while True:
			command = raw_input('')
			if not command:
				break
			else:
				print 'ini command' : command
				try:
					function = getattr(self,command[:4].strip().upper())
					function(command)
				except Exception,e:
					print 'ERROR:',e

	def USER(self,command):
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def PASS(sell,command):
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()


def main():
	newclient = ('localhost',12345)
	newclient.run()

if __name__ == '__main__':
	main()