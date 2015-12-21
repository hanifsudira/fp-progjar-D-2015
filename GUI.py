from Tkinter import * #import Tk, Text, BOTH, W, N, E, S
from ttk import * #Frame, Button, Label, Style
import tkMessageBox
import pickle
class GUI(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
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
		
	def convert(self , tog=[0]):
		tog[0] = not tog[0]
		if tog[0]:
			abtn.configure(text='Stop')
		else:
			self.configure(text='Start')

	def initUI(self):
		self.parent.title("Simple FTP Server")
		self.pack(fill=BOTH, expand=True)

		self.columnconfigure(1, weight=1)
		self.columnconfigure(3, pad=7)
		self.rowconfigure(3, weight=1)
		self.rowconfigure(5, pad=7)
		
		lbl = Label(self, text="Command Line")
		lbl.grid(sticky=W, pady=4, padx=5)
		
		area = Text(self)
		area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=E+W+S+N)
		area.insert('1.0',"wewewewew")

		abtn = Button(self, text="Start", command=self.convert)
		abtn.grid(row=1, column=3)

		ubtn = Button(self, text="Tambah User", command = self.add_user)
		ubtn.grid(row=4 , column=3)
		
		hbtn = Button(self, text="About", command = self.about)
		hbtn.grid(row=5, column=0, padx=5)

		obtn = Button(self, text="Quit", command = self.ask_quit)
		obtn.grid(row=5, column=3)        

if __name__ == '__main__':
	root = Tk()
	root.geometry("640x480")
	root.resizable(width=False, height=False)
	app = GUI(root)
	root.mainloop()