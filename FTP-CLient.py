#Final Project Program Jaringan Kelas D 2015
#Author : Guruh, Burhan, Ghulam, Hanif

import socket 

class Client:
	def __init__(self,(ip,port)):
		self.serverip 	= ip
		self.port 		= port
		self.server 	= None
		self.data_sock	= None
		self.recvdata	= ""

	def opensocket(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect((self.serverip,self.port))
		welcome_msg = self.server.recv(1024)
		print welcome_msg.strip()
	
	def run(self):
		self.opensocket()
		while True:
			command = raw_input('')
			if not command:
				break
			else:
				print 'ini command' , command
				try:
					function = getattr(self,command[:4].strip().upper())
					function(command)
				except Exception,e:
					print 'ERROR:',e

	def USER(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def PASS(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def HELP(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
	
	def QUIT(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
	
	def SYST(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
	
	def TYPE(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def PWD(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def CWD(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def CDUP(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
	
	def MKD(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def RMD(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	# def PASV():
	# 	self.server.send('PASV\r\n')
	# 	msg = self.server.recv(1024)
	# 	print msg.strip()
	# 	data_port = str(msg.strip().split('(')[1][:-2])
	# 	p1=int(data_port.split(',')[4])
	# 	p2=int(data_port.split(',')[5])
	# 	data_port = p1 * 256 + p2
	# 	self.data = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 	self.data.connect(('localhost', data_port))
	# 	self.recvdata=self.data.recv(1024)
	# 	print self.recvdata

	def LIST(self,command):
		self.server.send('PASV\r\n')
		msg = self.server.recv(1024)
		data = msg.strip() 
		print msg.strip()
		if "Entering Passive Mode" in msg:
			tp = data.split('(')[1].split(')')[0].split(',')
			port = int(tp[4])*256+int(tp[5])
			self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.data_sock.connect(('localhost',port))
			self.server.send(command)
			self.recvdata=self.data_sock.recv(1024)
			print self.recvdata.strip()


def main():
	newclient = Client(('localhost',12345))
	newclient.run()

if __name__ == '__main__':
	main()