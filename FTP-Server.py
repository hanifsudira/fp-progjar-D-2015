#Final Project Program Jaringan Kelas D 2015
#Author : Guruh, Burhan, Ghulam, Hanif

import socket
import threading as t
import os

#list untuk menampung username dan password
user = [('hanif','123'),('burhan','123'),('ghulam','123')]

#define ip, port and max client
ip 			= 'localhost'
port 		= 12345
max_client 	= 10

class FTPServerFunction(t.Thread):
	def __init__(self,(connection,address)):
		self.connection	= connection
		self.address 	= address
		t.Thread.__init__(self)
		self.username = ''

	def run(self):
		self.connection.send('220 Welcome!\r\n')
		while True:
			command = self.connection.recv(1024)
			if not command:
				break
			else:
				print 'ini command : ', command
				try:
					function = getattr(self,command[:4].strip().upper())
					function(command)
				except Exception,e:
					print 'ERROR:',e
					self.connection.send('500 Sorry.\r\n')

	def USER(self,command):
		username = command.strip().split(' ')[1]
		self.username = username
		kirim = '331 Password required for '+username+'\r\n'
		self.connection.send(kirim)

	def PASS(self,command):
		password = command.strip().split(' ')[1]
		flag = False
		for i in range(len(user)):
			if self.username == user[i][0] and password == user[i][1]:
				flag = True	
		if flag:
			self.connection.send('230 Logged on\r\n')
		else:
			self.connection.send('530 Login or password incorrect!\r\n')
			exit()

class FTPServer(t.Thread):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((ip,port))
		t.Thread.__init__(self)

	def run(self):
		self.sock.listen(max_client)
		while True:
			thclient 		= FTPServerFunction(self.sock.accept())
			thclient.daemon	= True
			thclient.start()

	def stop(self):
		self.sock.close()

def main():
	FTP 		= FTPServer()
	FTP.daemon	= True
	FTP.start()
	print 'connect on ', ip,':',port
	raw_input('Enter untuk mengakhiri...\n')
	FTP.stop()

main()