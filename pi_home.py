#! python3

import common
from config import config
import os
import pi_screen
import sys
import tkinter as tk


class HomeGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        if os.name == "nt":
            self.config(width=800, height=480)
            self.width = 800
            self.height = 480
            self.pack_propagate(0)
        else:
            self.attributes('-fullscreen', True)
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
        self.focus_set()
        self.bind_all("<Escape>", lambda e: e.widget.quit())
        self.wm_title("Raspberry Pi Home Base")
        self.idle_screen = None
        self.config(bg="dark gray")
        self.config(cursor="left_ptr")
        self.home_screen = pi_screen.HomeScreen(self)
        self.update_idletasks()
        x = (self.width/2) - (self.home_screen.winfo_reqwidth()/2)
        y = (self.height / 2) - (self.home_screen.winfo_reqheight() / 2)
        self.home_screen.place(x=x, y=y)
        self.idle_delay = config["Idle Delay"]
        self.check_for_updates()
        self.mouse_hide_timer_id = None
        self.show_mouse()
        self.bind_all("<Motion>", self.show_mouse)
        self.timed_events = {}
        [self.add_event(event_name) for event_name in config["Timed Events"]]

    def every(self, ms, func=None, *args):
        super().after(ms, func, *args)
        self.after(ms, self.every, ms, func, *args)

    def add_event(self, event_name):
        event_data = config["Timed Events"][event_name]
        try:
            module = event_data["command"]["module"]
            function = event_data["command"]["function"]
            if module != "":
                exec("import %s" % module)
                command = eval("%s.%s" % (module, function))
            else:
                command = eval("self.%s" % function)
            event_data["command"] = command
        except KeyError:
            print(event_data)
            raise KeyError("No command specified for timed event!")
        self.every(event_data["time"], command)

    def screen_lock(self):
        if self.idle_delay == config["Idle Delay"]:
            self.idle_delay = config["Locked Delay"]
        else:
            self.idle_delay = config["Idle Delay"]

    def update_idle_timer(self, event=None):
        # Check the time and see if we should go idle, if not update the time again
        if self.idle_screen:
            if common.idle() < self.idle_delay:
                self.do_home_screen()
        else:
            if common.idle() >= self.idle_delay:
                self.do_idle_screen()

    def do_idle_screen(self, event=None):
        self.idle_delay = config["Idle Delay"]
        self.idle_screen = pi_screen.HomeIdleScreen(self)

    def do_home_screen(self, event=None):
        if self.idle_screen:
            self.idle_screen.destroy()
            self.idle_screen = None

    def check_for_updates(self, event=None):
        updated = common.git_update()
        if updated:
            os.execl(sys.executable, sys.executable, *sys.argv)

    def hide_mouse(self, event=None):
        self.config(cursor="none")
        self.mouse_hide_timer_id = None

    def show_mouse(self, event=None):
        if self.mouse_hide_timer_id:
            self.after_cancel(self.mouse_hide_timer_id)
        self.config(cursor=config["Cursor"])
        self.mouse_hide_timer_id = self.after(config["Mouse Hide Delay"], self.hide_mouse)


if __name__ == "__main__":
    home = HomeGui()
    home.mainloop()
