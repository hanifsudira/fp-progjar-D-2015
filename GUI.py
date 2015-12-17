from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style
import tkMessageBox

class GUI(Frame):
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.initUI()

	def about(self):
		tkMessageBox.showinfo("About", "Simple FTP Server\n\nGuruh Arya Sena\t5113100010\nBurhanudin Rasyid\t5113100046\nM. Ghulam Fajri\t5113100094\nHanif Sudira\t5113100184")

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

		abtn = Button(self, text="Start")
		abtn.grid(row=1, column=3)

		cbtn = Button(self, text="Stop")
		cbtn.grid(row=2, column=3, pady=4)

		ubtn = Button(self, text="Add User")
		ubtn.grid(row=4 , column=3)
		
		hbtn = Button(self, text="About", command = self.about)
		hbtn.grid(row=5, column=0, padx=5)

		obtn = Button(self, text="OK")
		obtn.grid(row=5, column=3)        

if __name__ == '__main__':
	root = Tk()
	root.geometry("640x480")
	root.resizable(width=False, height=False)
	app = GUI(root)
	root.mainloop()