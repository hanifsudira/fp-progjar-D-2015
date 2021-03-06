from Tkinter import * #import Tk, Text, BOTH, W, N, E, S
from ttk import * #Frame, Button, Label, Style
from time import sleep
import tkMessageBox
import pickle
import socket
import threading as t
import os
import select

#abtn = Button

currentdirectory = os.path.abspath('.')
allow_delete = True

#def callback():
#	 execfile("MultiClient-FTP.py")


user = [('a','1')]

ip 		= 'localhost'
port 		= 12345
max_client 	= 10


class Server:
	def __init__(self):
		self.host = ip
		self.port = port
		self.backlog = 5
		self.size = 1024
		self.server = None
		self.threads = []
		#self.runrun=False

	def open_socket(self):        
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.host,self.port))
		self.server.listen(max_client)
		
	def run(self, runrun=None):
		self.open_socket()
		input = [self.server, sys.stdin]
		running = 1
		while running:
			inputready,outputready,exceptready = select.select(input,[],[])
			for s in inputready:
				if s == self.server:
					# handle the server socket
					c = Client(self.server.accept())
					print c
					c.start()
					self.threads.append(c)
				elif s == sys.stdin:
					# handle standard input
					junk = sys.stdin.readline()
					running = 0
		# close all threads
		self.server.close()
		for c in self.threads:
			c.join()


class Client(t.Thread):
	def __init__(self,(connection,address)):
		self.connection	= connection
		self.address 	= address
		t.Thread.__init__(self)
		self.username 	= ''
		self.rest=False
		self.pasv_mode	= False
		self.basedirectory = currentdirectory
		self.currentdirectory = self.basedirectory
		self.closeflag = True
		self.total = ""

	def run(self):
		self.connection.send('220 Welcome!. ini adalah FTP sederhana kami :)\r\n')
		# while True:
		# 	command = self.connection.recv(1024)	
		# 	if not command and self.closeflag :
		# 		break
		# 	else:
		# 		print 'ini command : ', command.strip()
		# 		try:
		# 			function = getattr(self,command[:4].strip().upper())
		# 			function(command)
		# 		except Exception,e:
		# 			print 'ERROR:',e
		# 			self.connection.send('500 Syntax Error.\r\n')

		running = 1
		while running:
			command = self.connection.recv(1024)
			if command and self.closeflag:
				print 'ini command : ',command.strip()
				try:
					function = getattr(self,command[:4].strip().upper())
					function(command)
				except Exception,e:
					print 'ERROR:',e
					self.connection.send('500 Syntax Error.\r\n')
			else:
				self.connection.close()
				running = 0

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
			self.closeflag = False
			#self.connection.close()

	def QUIT(self,command):
		self.connection.send('221 Goodbye.\r\n')
		self.closeflag = False
		#self.connection.close()

	def MKD(self,command):
		dirname=os.path.join(self.currentdirectory,command[4:-2])
		os.mkdir(dirname)
		self.connection.send('257 Directory created.\r\n')

	def RMD(self,command):
		dirname=os.path.join(self.currentdirectory,command[4:-2])
		if allow_delete:
			os.rmdir(dirname)
			self.connection.send('250 Directory deleted.\r\n')
		else:
			self.connection.send('450 Not allowd.\r\n')

	def DELE(self,command):
		filename=os.path.join(self.currentdirectory,command[5:-2])
		if allow_delete:
			os.remove(filename)
			self.connection.send('250 File delete.\r\n')
		else:
			self.connection.send('450 Not allowed.\r\n')

	def AUTH(self,command):
		self.connection.send('530 Please login with USER and PASS\r\n')

	def SYST(self,command):
		reply = "215 "+os.name+" "+platform.system()+" "+platform.system()+"\r\n"
		self.connection.send(reply)

	def TYPE(self,command):
		self.mode = command[5]
		self.connection.send('200 Binary mode.\r\n')

	def REST(self,command):
		self.pos=int(command[5:-2])
		self.rest=True
		self.connection.send('250 File position reseted.\r\n')

	def HELP(self,command):
		pesan = "214-The following commands are reconized\n USER PASS MKD RMD DELE SYST AUTH SYST TYPE REST\n HELP RETR STOR PWD CWD CDUP PASV RNFR RNTO LIST\n214 Help OK.\r\n"
		self.connection.send(pesan)

	def RETR(self,command):
		filename=os.path.join(self.currentdirectory,command[5:-2])
		print 'sedang mendownload:',filename
		if self.mode=='I':
			fileinput=open(filename,'rb')
		else:
			fileinput=open(filename,'r')
		self.connection.send('150 Opening data connection.\r\n')
		if self.rest:
			fileinput.seek(self.pos)
			self.rest=False
		data= fileinput.read(1024)
		self.start_datasock()
		while data:
			self.datasock.send(data)
			data=fileinput.read(1024)
		fileinput.close()
		self.stop_datasock()
		self.connection.send('226 Transfer complete.\r\n')

	def STOR(self,command):
		filename=os.path.join(self.currentdirectory,command[5:-2])
		print 'sedang upload',filename
		if self.mode=='I':
			fileoutput=open(filename,'wb')
		else:
			fileoutput=open(filename,'w')
		self.connection.send('150 Opening data connection.\r\n')
		self.start_datasock()

		while True:
			data=self.datasock.recv(1024)
			if not data: break
			fileoutput.write(data)
		fileoutput.close()
		self.stop_datasock()
		self.connection.send('226 Transfer complete.\r\n')


	def PWD(self,command):
		#relpath -> Return a relative filepath to path either from the current directory or from an optional start directory
		printworkingdirectory = os.path.relpath(self.currentdirectory,self.basedirectory)
		if printworkingdirectory == '.':
			printworkingdirectory = '/'
		else:
			printworkingdirectory = '/' + printworkingdirectory
		self.connection.send('257 \"%s\"\r\n' % printworkingdirectory)


	def CWD(self,command):
		changeworkingdirectory = command[4:-2]
		if changeworkingdirectory =='/':
			self.currentdirectory =self.basedirectory
		elif changeworkingdirectory[0]=='/':
			self.currentdirectory=os.path.join(self.basedirectory,changeworkingdirectory[1:])
		else:
			self.currentdirectory=os.path.join(self.currentdirectory,changeworkingdirectory)
		self.connection.send('250 OK.\r\n')

	def CDUP(self,command):
		if not os.path.samefile(self.currentdirectory,self.basedirectory):
			self.currentdirectory=os.path.abspath(os.path.join(self.currentdirectory,'..'))
		self.connection.send('200 OK.\r\n')

	def PASV(self,command):
		self.pasv_mode 	= True
		self.serversock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.serversock.bind((ip,0))
		self.serversock.listen(1)
		now_ip,now_port	= self.serversock.getsockname()
		#print 'port for passive mode:',now_port
		self.connection.send('227 Entering Passive Mode (%s,%u,%u).\r\n' %(','.join(now_ip.split('.')), now_port>>8&0xFF, now_port&0xFF))

	def RNFR(self,command):
		self.renamefilename=os.path.join(self.currentdirectory,command[5:-2])
		self.connection.send('350 Ready.\r\n')

	def RNTO(self,command):
		filename = os.path.join(self.currentdirectory,command[5:-2])
		os.rename(self.renamefilename,filename)
		self.connection.send('250 File renamed.\r\n')

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

	def LIST(self,command):
		self.total = ""
		self.connection.send('150 Here comes the directory listing.\r\n')
		print 'list:', self.currentdirectory
		self.start_datasock()
		for t in os.listdir(self.currentdirectory):
			k=self.toListItem(os.path.join(self.currentdirectory,t))
			self.total+=(k+'\r\n')
		self.datasock.send(self.total)
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


class STDText(Text):
   def __init__(self, parent):
     Text.__init__(self, parent)

   def write(self, stuff):
     self.insert("end", stuff)
     self.yview_pickplace("end")


class GUI(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)

		self.parent = parent
		self.runrun=False
		self.initUI()

	def about(self):
		tkMessageBox.showinfo("About", "Simple FTP Server\n\nGuruh Arya Sena\t5113100010\nBurhanudin Rasyid\t5113100046\nM. Ghulam Fajri\t5113100094\nHanif Sudira\t5113100184")

	def ask_quit(self):
		if tkMessageBox.askokcancel("Quit", "Anda Yakin Keluar?"):
			self.quit()
			
	def add_user(self):

		def function():
			flag = False
			username = e1.get()
			password = e2.get()
			inp = (username,password)
			if inp:
				with open('user.txt','rb') as f:
					my_list = pickle.load(f)
					print my_list
				for x in range(len(my_list)):
					if my_list[x][0] == inp[0]:
						flag = True
						break
				if flag:
					tkMessageBox.showerror("Error","User Telah Terdaftar")
				else:
					my_list.append(inp)
					masuk = pickle.dump(my_list)
					with open('user.txt','wb') as f:
						f.write(masuk)
					tkMessageBox.showinfo("Success","Berhasil Menambah User")
					print my_list
					flag = False


		newwin = Tk()
		newwin.geometry("300x100")
		newwin.title("Tambah User")
		newwin.resizable(width=False, height=False)
		
		Label(newwin, width=15, text="First Name").grid(row=0)
		Label(newwin, width=15, text="Last Name").grid(row=1)

		e1 = Entry(newwin)
		e2 = Entry(newwin)

		e1.grid(row=0, column=1)
		e2.grid(row=1, column=1)

		Button(newwin, text='Tambah', command=function).grid(row=3, column=1, sticky=W, pady=4)
		Button(newwin, text='Batal', command=newwin.quit).grid(row=3, column=0, sticky=W, pady=4)
		
	
	def initUI(self):
		#self.runrun=False
		self.parent.title("Simple FTP Server")
		self.pack(fill=BOTH, expand=True)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=7)
		
		lbl = Label(self, text="Command Line")
		lbl.grid(sticky=W, pady=4, padx=5)
		area = STDText(self)
		area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
		#area.insert('1.0',"wewewewew")
		sys.stdout=area		

		self.abtn = Button(self, text="Start", command=lambda:self.execute(True))
		self.abtn.grid(row=1, column=3)

		self.bbtn = Button(self, text="Stop", command=lambda:self.execute(False))
		self.bbtn.grid(row=2, column=3)		

		ubtn = Button(self, text="Tambah User", command = self.add_user)
		ubtn.grid(row=4 , column=3)
		
		hbtn = Button(self, text="About", command = self.about)
		hbtn.grid(row=5, column=0, padx=5)

		obtn = Button(self, text="Quit", command = self.ask_quit)
		obtn.grid(row=5, column=3) 
       
	def execute(self, runrun=None):
 	 if runrun is not None:
	  self.runrun = runrun
	 if self.runrun:
	  FTP = Server()
	  print 'connect on ', ip,':',port
	  FTP.run()
	  self.parent.after(5000, self.execute)	
	  #raw_input('Enter untuk mengakhiri...\n')
	
	#def convert(self , tog=[0]):
	#	tog[0] = not tog[0]
	#	if tog[0]:
	#		self.abtn.config(text='Stop')
	#	else:
	#		self.abtn.config(text='Start', command=main)

	
	


if __name__ == '__main__':	
	root = Tk()
	root.geometry("640x480")
	root.resizable(width=False, height=False)
	app = GUI(root)
	root.mainloop()
