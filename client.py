from Tkinter import Tk, Text, TOP, BOTH, X, N, Y, LEFT, RIGHT, RAISED, TOP, W, BOTTOM,NW,NE,E,SW
from ttk import Frame, Label, Entry, Button, Style
import os
import socket 


currentdirectory = os.path.abspath('.')

def callback():
		execfile("FTP-CLient.py")

class Client:
	def __init__(self,(ip,port)):
		self.serverip 		= ip
		self.port 		= port
		self.server 		= None
		self.data_sock		= None
		self.recvdata		= ""
		self.currentdirectory	= currentdirectory
		self.isi		= ""
	
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
	
	def TYPESTOR(self):
		com="TYPE I\r\n"
		self.server.send(com)
		msg = self.server.recv(1024)
		print msg.strip()	

	def TYPERETR(self):
		com="TYPE A\r\n"
		self.server.send(com)
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

	def RNTO(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def RNFR(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def RMD(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

	def DELE(self,command):
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
	
	def PASV(self):
		command="PASV\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
		data = msg.strip() 
		if "Entering Passive Mode" in msg:
			tp = data.split('(')[1].split(')')[0].split(',')
			port = int(tp[4])*256+int(tp[5])
		return port 

	def LIST(self,command):
		port=self.PASV()
		self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.data_sock.connect(('localhost',port))
		self.server.send(command)
		self.recvdata=self.data_sock.recv(1024)
		print self.recvdata.strip()
		msg = self.server.recv(1024)
		print msg.strip()
		msg = self.server.recv(1024)
		print msg.strip()
	
	def STOR(self,command):
		filename=os.path.join(self.currentdirectory,command[5:])
		self.TYPESTOR()
		port=self.PASV()
		self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.data_sock.connect(('localhost',port))

		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()
		
		f = open(filename,'rb')
		l = f.read()
		f.close()
		self.data_sock.sendall(l)
		self.data_sock.close()
		
		msg = self.server.recv(1024)
		print msg.strip()

	def RETR(self,command):
		filename=os.path.join(self.currentdirectory,command[5:])
		self.TYPERETR()
		port=self.PASV()
		self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.data_sock.connect(('localhost',port))
		#self.data_sock.recv(1024)
		#self.data_sock.recv(1024)
		command+="\r\n"
		self.server.send(command)
		msg = self.server.recv(1024)
		print msg.strip()

		with open (filename, 'wb') as f:
			self.isi = self.data_sock.recv(4096)
			while (self.isi):
				if not self.isi: break
				else:
					f.write(self.isi)
					self.isi = self.data_sock.recv(4096)

		msg = self.server.recv(1024)
		print msg.strip()

class Example(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		 
		self.parent = parent
		self.initUI()
		
	def initUI(self):
		
		self.parent.title("Simple FTP-Client")
		self.pack(fill=BOTH, expand=True)
	
		# self.parent.title("Buttons") 
				
		#frame2 = Frame(self)
		#frame2.pack(anchor=W,side=LEFT)
		#lbl2 = Label(frame2, text="Command Line", width=6)
		#lbl2.pack(fill=X,anchor=W,expand=True,padx=5, pady=5)        
		#txt2 = Text(frame2)
		#txt2.pack(fill=X,side=BOTTOM,pady=5, padx=5)           

		frame3 = Frame(self, width=400, height=500)
		frame3.pack(side=BOTTOM,anchor=NW)
		lbl3 = Label(frame3, text="Command Line", width=6)
		lbl3.pack(fill=X,anchor=NE,expand=True,padx=5, pady=5)        
		txt = Text(frame3)
		txt.pack(fill=BOTH,pady=5, padx=5)
	        wid = frame3.winfo_id()
		os.system('xterm -into %d -geometry 400x400 -sb &' % wid)
		
		     
		
		f1 = Frame(self)
		f1.pack(fill=X,side=LEFT, anchor=NW, padx=5, pady=10)
		lb=Label(f1, text="Host:").grid(row=0, column=0)
		e1 = Entry(f1)
		e1.grid(row=0, column=1, padx=1)
		
		f2 = Frame(self)
		f2.pack(fill=X,side=LEFT, anchor=NW, padx=5, pady=10)
		lb2=Label(f2, text="Username:").grid(row=0, column=2)
		e2 = Entry(f2)
		e2.grid(sticky=N,row=0, column=3, padx=5)

		f3 = Frame(self)
		f3.pack(fill=X,side=LEFT, anchor=NW, padx=5, pady=10)
		lb=Label(f3, text="Password:").grid(row=0, column=0)
		e3 = Entry(f3)
		e3.grid(row=0, column=1, padx=5)
		
		f4 = Frame(self)
		f4.pack(fill=X,side=LEFT, anchor=NW, padx=5, pady=10)
		lb4=Label(f4, text="Port:").grid(row=0, column=2)
		e4 = Entry(f4)
		e4.grid(row=0, column=3, padx=5)

		connectButton = Button(self, text="Connect", command=callback)
		connectButton.pack(expand=True,fill=X,side=LEFT, anchor=NW, padx=10, pady=10)
		
#def runnewclient(self, event)
 #teks = open('FTP-CLient.py', 'r').read()
		

def main():
	root = Tk()
	root.geometry("1300x720")
	app = Example(root)
	root.mainloop()  
	root.resizable(width=False, height=False)
	

if __name__ == '__main__':
	main()  
