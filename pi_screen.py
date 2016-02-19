import os
import time
import tkinter as tk


class Layer(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visible = False

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.visible = True

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.visible = True

    def pack_forget(self):
        super().pack_forget()
        self.visible = False

    def place_forget(self):
        super().place_forget()
        self.visible = False


class HomeScreen(Layer):
    def __init__(self, master):
        super().__init__(master, width=master.width, height=master.height)
        self.images = {"enceladus": tk.PhotoImage(file="enceladus.gif"),
                       "grand tour": tk.PhotoImage(file="grand_tour.gif")}
        self.enceladus_button = tk.Button(self, image=self.images["enceladus"], bd=0)
        self.enceladus_button.pack(side=tk.LEFT)
        self.grand_tour_button = tk.Button(self, image=self.images["grand tour"], bd=0)
        self.grand_tour_button.pack(side=tk.LEFT)


class HomeIdleScreen(Layer):
    def __init__(self, master):
        super().__init__(master, bg='black')
        self.update_time_id = None
        self.time = tk.Label(self,
                             font="Ariel 80",
                             fg='dark orange',
                             bg='black',
                             anchor=tk.N)
        self.date = tk.Label(self,
                             font="Ariel 40",
                             fg='dark orange',
                             bg='black',
                             anchor=tk.N)
        self.update_time()

    def update_time(self, event=None):
        self.time.config(text=time.strftime("%H:%M:%S"))
        self.date.config(text=time.strftime("%A, %B %d %Y"))
        self.time.pack(side=tk.TOP)
        self.date.pack(side=tk.TOP)
        self.update_time_id = self.after(50, self.update_time)

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.update_time()

    def place_forget(self):
        super().place_forget()
        self.after_cancel(self.update_time_id)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.update_time()

    def pack_forget(self):
        super().pack_forget()
        self.after_cancel(self.update_time_id)
