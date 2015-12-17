#Final Project Program Jaringan Kelas D 2015
#Author : Guruh, Burhan, Ghulam, Hanif

import socket
import threading as t
import os
import platform
import time

#list untuk menampung username dan password
user = [('hanif','123'),('burhan','123'),('ghulam','123'),('guruh','123')]

#define ip, port and max client
ip 			= 'localhost'
port 		= 12345
max_client 	= 10

#define another
currentdirectory = os.path.abspath('.')
allow_delete = False

class FTPServerFunction(t.Thread):
	def __init__(self,(connection,address)):
		self.connection	= connection
		self.address 	= address
		t.Thread.__init__(self)
		self.username 	= ''
		self.pasv_mode	= False
		self.basedirectory = currentdirectory
		self.currentdirectory = self.basedirectory

	def run(self):
		self.connection.send('220 Welcome!. ini adalah FTP sederhana kami :)\r\n')
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
					self.connection.send('500 Syntax Error.\r\n')

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

	def QUIT(self,command):
		self.connection.send('221 Goodbye.\r\n')
		exit()

	def AUTH(self,command):
		self.connection.send('530 Please login with USER and PASS\r\n')

	def SYST(self,command):
		reply = "215 "+os.name+" "+platform.system()+" "+platform.system()+"\r\n"
		self.connection.send(reply)

	def TYPE(self,command):
		self.mode = command[5]
		self.connection.send('200 Binary mode.\r\n')

	def PWD(self,command):
		#relpath -> Return a relative filepath to path either from the current directory or from an optional start directory
		printworkingdirectory = os.path.relpath(self.currentdirectory,self.basedirectory)
		if printworkingdirectory == '.':
			printworkingdirectory = '/'
		else:
			printworkingdirectory = '/' + printworkingdirectory
		self.connection.send('257 \"%s\"\r\n' % printworkingdirectory)

	def PASV(self,command):
		self.pasv_mode 	= True
		self.serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.serversock.bind((ip,0))
		self.serversock.listen(1)
		now_ip,now_port	= self.serversock.getsockname()
		#print 'port for passive mode:',now_port
		self.connection.send('227 Entering Passive Mode (%s,%u,%u).\r\n' %(','.join(now_ip.split('.')), now_port>>8&0xFF, now_port&0xFF))

	def start_datasock(self):
		if self.pasv_mode:
			self.datasock, addr = self.serversock.accept()
			print 'connect:', addr
		else:
			self.datasock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			self.datasock.connect((self.dataAddr,self.dataPort))

	def stop_datasock(self):
		self.datasock.close()
		if self.pasv_mode:
			self.serversock.close()

	def LIST(self,cmd):
		self.connection.send('150 Here comes the directory listing.\r\n')
		print 'list:', self.currentdirectory
		self.start_datasock()
		for t in os.listdir(self.currentdirectory):
			k=self.toListItem(os.path.join(self.currentdirectory,t))
			self.datasock.send(k+'\r\n')
		self.stop_datasock()
		self.connection.send('226 Directory send OK.\r\n')

	def toListItem(self,fn):
		st=os.stat(fn)
		fullmode='rwxrwxrwx'
		mode=''
		for i in range(9):
			mode+=((st.st_mode>>(8-i))&1) and fullmode[i] or '-'
		d=(os.path.isdir(fn)) and 'd' or '-'
		ftime=time.strftime(' %b %d %H:%M ', time.gmtime(st.st_mtime))
		return d+mode+' 1 user group '+str(st.st_size)+ftime+os.path.basename(fn)

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


if __name__ == '__main__':
	FTP 		= FTPServer()
	FTP.daemon	= True
	FTP.start()
	print 'connect on ', ip,':',port
	raw_input('Enter untuk mengakhiri...\n')
	FTP.stop()