import common
import config
import multiprocessing
import os
import time
import tkinter as tk


def construct_element(master, data):
    """
    Construct a button from the data passed in.
    :param master: str
    :param data: dict
    :return: tk.Button
    """
    # See what imports we need to do:
    if "module" in data:
        module = data["module"]
        exec("import %s" % module)
    else:
        module = "tk"
    if "config" in data and "command" in data["config"]:
        command_module = data["config"]["command"]["module"]
        function = data["config"]["command"]["function"]
        if command_module != "":
            exec("import %s" % command_module)
            command = "%s.%s" % (command_module, function)
        else:
            command = "%s" % function
        data["config"]["command"] = command

    element = eval("%s.%s(master)" % (module, data["type"]))
    for option in data["config"]:
        value = data["config"][option]
#            print(option, ":", value)
        eval("element.config(%s=%s)" % (option, value))
    element.place(x=data["x"], y=data["y"])
    print(type(element))
    return element


class Screen(tk.Frame):
    def __init__(self, master, name, data):
        """
        :param master: HomeGui
        :return:
        """
        super().__init__(master)
        self.name = name
        self.config(width=master.width, height=master.height)
        for item in data:
            if item == "elements":
                self.elements = {element_name:construct_element(self, data[item][element_name])
                                 for element_name in data[item]}
            else:
                eval("self.config(%s=%s)" % (item, data[item]))

        self.quit_button = tk.Button(self, bd=0,
                                     text="X",
                                     font="Ariel 8",
                                     command=self.master.quit)
        self.update_idletasks()
        self.quit_button.place(x=self.winfo_reqwidth() - self.quit_button.winfo_reqwidth(), y=0)
        self.shell_process = None


class HomeIdleScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master, bg='black')
        if os.name == "nt":
            self.config(width=800, height=480)
            self.width = 800
            self.height = 480
            self.pack_propagate(0)
            self.geometry(self.master.winfo_geometry())
        else:
            self.attributes('-fullscreen', True)
            self.attributes("-topmost", True)
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
        self.config(bg="black", cursor="none")
        self.update_time_id = None
        self.day = tk.Label(self,
                            font=self.master.settings["Date Font"],
                            bg='black',
                            anchor=tk.N)
        self.time = tk.Label(self,
                             font=self.master.settings["Time Font"],
                             bg='black',
                             anchor=tk.N)
        self.date = tk.Label(self,
                             font=self.master.settings["Date Font"],
                             bg='black',
                             anchor=tk.N)
        self.update_time()

    def update_time(self, event=None):
        localtime = time.localtime()
        local_min = localtime.tm_hour * 60 + localtime.tm_min
        day_start = time.strptime(self.master.settings["Clock Day Start"], "%H:%M")
        day_min = day_start.tm_hour * 60 + day_start.tm_min
        night_start = time.strptime(self.master.settings["Clock Night Start"], "%H:%M")
        night_min = night_start.tm_hour * 60 + night_start.tm_min
        if night_min <= local_min or \
                        day_min >= local_min:
            self.day.config(fg=self.master.settings["Clock Night Color"])
            self.time.config(fg=self.master.settings["Clock Night Color"])
            self.date.config(fg=self.master.settings["Clock Night Color"])
        else:
            self.day.config(fg=self.master.settings["Clock Day Color"])
            self.time.config(fg=self.master.settings["Clock Day Color"])
            self.date.config(fg=self.master.settings["Clock Day Color"])
        self.day.config(text=time.strftime("%A"))
        self.time.config(text=time.strftime("%H:%M"))
        self.date.config(text=time.strftime("%B %d %Y"))
        # Place time in the center and then date just below the bottom of it
        x = (self.width / 2) - (self.time.winfo_reqwidth() / 2)
        y = (self.height / 2) - (self.time.winfo_reqheight() / 2)
        self.time.place(x=x, y=y)
        x = (self.width / 2) - (self.date.winfo_reqwidth() / 2)
        y = self.time.winfo_y() + self.time.winfo_reqheight()
        self.date.place(x=x, y=y)
        x = (self.width / 2) - (self.day.winfo_reqwidth() / 2)
        y = self.time.winfo_y() - self.day.winfo_reqheight()
        self.day.place(x=x, y=y)
        self.update_time_id = self.after(50, self.update_time)
