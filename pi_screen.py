import os
import time
import tkinter as tk
import webbrowser


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
        super().__init__(master)
        self.config(width=master.width, height=master.height)
        self.images = {"enceladus": tk.PhotoImage(file=os.path.dirname(__file__) + os.sep + "enceladus.gif"),
                       "grand tour": tk.PhotoImage(file=os.path.dirname(__file__) + os.sep + "grand_tour.gif")}
        self.enceladus_button = tk.Button(self, bd=0,
                                          image=self.images["enceladus"],
                                          command=master.screen_lock)
        self.enceladus_button.pack(side=tk.LEFT)
        self.grand_tour_button = tk.Button(self, bd=0,
                                           image=self.images["grand tour"],
                                           command=self.open_browser)
        self.grand_tour_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self, bd=0,
                                     text="X",
                                     font="Ariel 8",
                                     command=self.master.quit)
        self.update_idletasks()
        self.quit_button.place(x=self.winfo_reqwidth()-self.quit_button.winfo_reqwidth(), y=0)

    @staticmethod
    def open_browser(event=None):
        webbrowser.open("http://www.google.com")


class HomeIdleScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master, bg='black')
        self.attributes('-fullscreen', True)
        self.config(bg="black", cursor="none")
        self.attributes("-topmost", True)
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
        # Place time in the center and then date just below the bottom of it
        x = (self.winfo_screenwidth()/2) - (self.time.winfo_reqwidth()/2)
        y = (self.winfo_screenheight()/2) - (self.time.winfo_reqheight()/2)
        self.time.place(x=x, y=y)
        x = (self.winfo_screenwidth()/2) - (self.date.winfo_reqwidth()/2)
        y = self.time.winfo_y() + self.time.winfo_reqheight()
        self.date.place(x=x, y=y)
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
