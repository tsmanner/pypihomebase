import pi_home
import time
import tkinter as tk


class Layer(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.visible = False

    def pack(self, *args, **kwargs):
        tk.Frame.pack(self, *args, **kwargs)
        self.visible = True

    def place(self, *args, **kwargs):
        tk.Frame.place(self, *args, **kwargs)
        self.visible = True

    def pack_forget(self):
        tk.Frame.pack_forget(self)
        self.visible = False

    def place_forget(self):
        tk.Frame.place_forget(self)
        self.visible = False


class HomeScreen(Layer):  # TODO this doesn't display!
    def __init__(self, master):
        Layer.__init__(self, master, width=master.width, height=master.height)
        self.box1 = tk.LabelFrame(self, text="BOX 1")
        self.box1.pack(side=tk.LEFT)
        self.box2 = tk.LabelFrame(self, text="BOX 2")
        self.box2.pack(side=tk.LEFT)


class HomeIdleScreen(Layer):
    def __init__(self, master):
        Layer.__init__(self, master, bg='black')
        self.time = tk.Label(self,
                             font="Ariel 40",
                             fg='dark orange',
                             bg='black',
                             anchor=tk.N)
        self.update_time()

    def update_time(self, event=None):
        self.time.config(text=str(time.asctime()))
        self.time.pack()
        self.after(50, self.update_time)

