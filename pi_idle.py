import pi_home
import time
import tkinter as tk


class HomeIdleScreen(pi_home.Layer):
    def __init__(self, master):
        pi_home.Layer.__init__(self, master, bg='black', width=800, height=400)
        self.time = tk.Label(self,
                             font="Ariel 40",
                             fg='dark orange',
                             bg='black',
                             anchor=tk.N)
        self.update_time()
        print(self.time.winfo_reqwidth(), self.time.winfo_reqheight())

    def update_time(self, event=None):
        self.time.config(text=str(time.asctime()))
        self.time.place(x=400-(self.time.winfo_reqwidth()/2), y=200-(self.time.winfo_reqheight()/2))
        self.after(50, self.update_time)

