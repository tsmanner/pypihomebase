import common
import multiprocessing
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
                       "grand tour": tk.PhotoImage(file=os.path.dirname(__file__) + os.sep + "grand_tour.gif"),
                       "launch": tk.PhotoImage(file=os.path.dirname(__file__) + os.sep + "launch.gif")}
        self.screen_lock_button = tk.Button(self, bd=0,
                                            image=self.images["enceladus"],
                                            command=master.screen_lock)
        self.screen_lock_button.pack(side=tk.LEFT)
        self.open_browser_button = tk.Button(self, bd=0,
                                             image=self.images["grand tour"],
                                             command=self.open_browser)
        self.open_browser_button.pack(side=tk.LEFT)
        self.open_shell_button = tk.Button(self, bd=0,
                                           image=self.images["launch"],
                                           command=self.open_shell)
        self.open_shell_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self, bd=0,
                                     text="X",
                                     font="Ariel 8",
                                     command=self.master.quit)
        self.update_idletasks()
        self.quit_button.place(x=self.winfo_reqwidth() - self.quit_button.winfo_reqwidth(), y=0)
        self.shell_process = None

    @staticmethod
    def open_browser(event=None):
        webbrowser.open("http://www.google.com")

    def open_shell(self, event=None):
        if self.shell_process:
            if os.name == "nt":
                pass # TODO how does this work in windows?
            else:
                elevate_str = "wmctrl -ia $(wmctrl -lp | awk -vpid={0} '$3==pid {print $1; exit}')"
                os.system(elevate_str.format(self.shell_process.pid))
        else:
            self.shell_process = multiprocessing.Process(target=common.open_shell)
            self.shell_process.start()


class HomeIdleScreen(tk.Toplevel):
    TEXT_COLOR = "red"

    def __init__(self, master):
        super().__init__(master, bg='black')
        if os.name == "nt":
            self.config(width=800, height=480)
            self.width = 800
            self.height = 480
            self.pack_propagate(0)
        else:
            self.attributes('-fullscreen', True)
            self.attributes("-topmost", True)
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
        self.config(bg="black", cursor="none")
        self.update_time_id = None
        self.time = tk.Label(self,
                             font="Ariel 80",
                             fg=self.TEXT_COLOR,
                             bg='black',
                             anchor=tk.N)
        self.date = tk.Label(self,
                             font="Ariel 40",
                             fg=self.TEXT_COLOR,
                             bg='black',
                             anchor=tk.N)
        self.update_time()

    def update_time(self, event=None):
        self.time.config(text=time.strftime("%H:%M:%S"))
        self.date.config(text=time.strftime("%A, %B %d %Y"))
        # Place time in the center and then date just below the bottom of it
        x = (self.width / 2) - (self.time.winfo_reqwidth() / 2)
        y = (self.height / 2) - (self.time.winfo_reqheight() / 2)
        self.time.place(x=x, y=y)
        x = (self.width / 2) - (self.date.winfo_reqwidth() / 2)
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
