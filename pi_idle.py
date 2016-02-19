import pi_home
import time
import tkinter as tk


class HomeIdleScreen(pi_home.Layer):
    def __init__(self, master):
        pi_home.Layer.__init__(self, master, bg='black', width=pi_home.WIDTH, height=pi_home.HEIGHT)
        self.time = tk.Label(self,
                             font="Ariel 40",
                             fg='dark orange',
                             bg='black',
                             anchor=tk.N)
        self.update_time()
        print(self.time.winfo_reqwidth(), self.time.winfo_reqheight())

    def update_time(self, event=None):
        self.time.config(text=str(time.asctime()))
        self.time.place(x=pi_home.WIDTH/2-(self.time.winfo_reqwidth()/2), y=pi_home.HEIGHT/2-(self.time.winfo_reqheight()/2))
        self.after(50, self.update_time)

