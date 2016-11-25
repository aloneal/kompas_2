from tkinter import *

class Application(Frame):
	"""GUI prilogenie 1"""
	def __init__(self, master):
		"""iniziiruet ramku"""
		super(Application, self).__init__(master)
		self.grid()
		self.bttn_click = 0
		self.create_widgets()
	def create_widgets(self):
		self.bttn = Button(self)
		self.bttn["text"] = "kolich klikov "
		self.bttn["command"] = self.update_count
		self.bttn.grid()
	def update_count(self):
		self.bttn_click += 1
		self.bttn["text"] = "count click " + str(self.bttn_click)

# osnovnaya chast'
root = Tk()
app = Application(root)
root.mainloop()