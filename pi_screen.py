import common
from config import config
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
        """
        :param master: HomeGui
        :return:
        """
        super().__init__(master)
        self.config(width=master.width, height=master.height)
        self.images = {"lock": tk.PhotoImage(file=os.path.dirname(__file__) +
                                                  os.sep +
                                                  config["HomeScreen Buttons"]["lock"]["image"]),
                       "browser": tk.PhotoImage(file=os.path.dirname(__file__) +
                                                     os.sep +
                                                     config["HomeScreen Buttons"]["browser"]["image"]),
                       "terminal": tk.PhotoImage(file=os.path.dirname(__file__) +
                                                      os.sep +
                                                      config["HomeScreen Buttons"]["terminal"]["image"])}
        self.screen_lock_button = tk.Button(self, bd=0,
                                            image=self.images["lock"],
                                            command=master.screen_lock)
        self.screen_lock_button.pack(side=tk.LEFT)
        self.open_browser_button = tk.Button(self, bd=0,
                                             image=self.images["browser"],
                                             command=common.open_browser)
        self.open_browser_button.pack(side=tk.LEFT)
        self.open_shell_button = tk.Button(self, bd=0,
                                           image=self.images["terminal"],
                                           command=self.open_shell)
        self.open_shell_button.pack(side=tk.LEFT)
        self.quit_button = tk.Button(self, bd=0,
                                     text="X",
                                     font="Ariel 8",
                                     command=self.master.quit)
        self.update_idletasks()
        self.quit_button.place(x=self.winfo_reqwidth() - self.quit_button.winfo_reqwidth(), y=0)
        self.shell_process = None

    def open_shell(self, event=None):
        if self.shell_process and self.shell_process.is_alive():
            if os.name == "nt":

                pass  # TODO how does this work in windows?
            else:
                print("Elevating existing shell process")
                elevate_str = "wmctrl -ia $(wmctrl -lp | awk -vpid={0} '$3==pid {print $1; exit}')"
                os.system(elevate_str.format(self.shell_process.pid))
        else:
            if self.shell_process:
                print("Joining derelict shell process")
                self.shell_process.join()
            print("Starting new shell")
            self.shell_process = multiprocessing.Process(target=common.open_shell)
            self.shell_process.start()


class HomeIdleScreen(tk.Toplevel):
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
                             bg='black',
                             anchor=tk.N)
        self.date = tk.Label(self,
                             font="Ariel 40",
                             bg='black',
                             anchor=tk.N)
        self.update_time()

    def update_time(self, event=None):
        localtime = time.localtime()
        day_start = time.strptime(config["Clock Day Start"], "%H:%M")
        night_start = time.strptime(config["Clock Night Start"], "%H:%M")
        if (night_start.tm_hour <= localtime.tm_hour and
                night_start.tm_min <= localtime.tm_min) or \
                (day_start.tm_hour >= localtime.tm_hour and
                 day_start.tm_min >= localtime.tm_min):
            self.time.config(fg=config["Clock Night Color"])
        else:
            self.time.config(fg=config["Clock Day Color"])
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
