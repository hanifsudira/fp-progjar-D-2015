from Tkinter import Tk, Text, TOP, BOTH, X, N, Y, LEFT, RIGHT, RAISED, TOP, W, BOTTOM,NW,NE,E,SW
from ttk import Frame, Label, Entry, Button, Style


class Example(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent)   
		 
		self.parent = parent
		self.initUI()

		
	def initUI(self):
		
		self.parent.title("Simple FTP-Client")
		self.pack(fill=BOTH, expand=True)
	
		# self.parent.title("Buttons")
		
		f3 = Frame(self)
		f3.pack(expand=True)
		lb=Label(f3, text="Password:").grid(row=0, column=0)
		e3 = Entry(f3)
		e3.grid(row=0, column=1, padx=5)
		
		# f4 = Frame(self)
		# f4.pack(expand=True)
		# lb4=Label(f4, text="Port:").grid(row=0, column=2)
		# e4 = Entry(f4)
		# e4.grid(row=0, column=3, padx=5)
		# self.style = Style()
		# self.style.theme_use("default")
		# self.pack(fill=BOTH, expand=True)
		# frame = Frame(self, relief=RAISED, borderwidth=1)
		# frame.pack(side=BOTTOM,fill=BOTH, expand=True)
		
		
		
			  
		
		
		# frame2 = Frame(self)
		# frame2.pack(anchor=W,side=LEFT)
		# lbl2 = Label(frame2, text="Command Line", width=6)
		# lbl2.pack(fill=X,anchor=W,expand=True,padx=5, pady=5)        
		# txt2 = Text(frame2)
		# txt2.pack(fill=X,side=BOTTOM,pady=5, padx=5)           

		frame3 = Frame(self)
		frame3.pack(side=BOTTOM,anchor=SW)
		lbl3 = Label(frame3, text="Command Line", width=6)
		lbl3.pack(fill=BOTH,anchor=SW,expand=True,padx=5, pady=5)        
		txt = Text(frame3)
		txt.pack(fill=BOTH,pady=5, padx=5)           
		
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
		
		connectButton = Button(self, text="Connect")
		connectButton.pack(expand=True,fill=X,side=LEFT, anchor=NW, padx=10, pady=10)
			
		# frame1 = Frame(self)
		# frame1.pack(fill=X)
		# lbl1 = Label(frame1, text="Title", width=6)
		# lbl1.pack(side=LEFT, padx=5, pady=5)           
		# entry1 = Entry(frame1)
		# entry1.pack(fill=Y, padx=0, expand=True)
		
		# frame2 = Frame(self)
		# frame2.pack(fill=X)
		# lbl2 = Label(frame2, text="Author", width=6)
		# lbl2.pack(side=LEFT, padx=5, pady=5)        
		# entry2 = Entry(frame2)
		# entry2.pack(fill=X, padx=5, expand=True)
		
		

def main():
  
	root = Tk()
	root.geometry("850x500")
	app = Example(root)
	root.mainloop()  
	root.resizable(width=False, height=False)
	

if __name__ == '__main__':
	main()  