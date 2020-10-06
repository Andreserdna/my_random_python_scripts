import os
import time
import tkinter as tk
from tkinter import ttk


class feed_mag_time:

	def __init__(self,timer=120):
		self.timer = timer

	def countdown(self):
		while self.timer <= 120:
			print("Couting down 2 minutes then mag feed time\n")
			print("{} seconds left until feeding time".format(self.timer))
			time.sleep(1)
			self.timer = self.timer - 1
			if self.timer == 0:
				print("Timer hit 0, time to feed mag")
				self.create_popup()
				self.timer = 120
				continue
	def create_popup(self):
		msg = "Time to feed the mag"
		FONT = ("Helvetica", 10)
		popup = tk.Tk()
		popup.wm_title("!")
		label = ttk.Label(popup,text=msg,font=FONT)
		label.pack(side="top",fill="x",pady=10)
		B1 = ttk.Button(popup,text="Okay",command=popup.destroy)
		B1.pack()
		popup.mainloop()
		return 


a = feed_mag_time()
while True:
	a.countdown()