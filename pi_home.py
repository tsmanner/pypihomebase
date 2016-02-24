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
        self.wm_title("12 Pine Echo Home")
        self.idle_screen = None
        self.config(bg="dark gray")
        self.config(cursor="left_ptr")
        self.idle_delay = 0
        self.home_screen = pi_screen.HomeScreen(self)
        self.update_idletasks()
        x = (self.width/2) - (self.home_screen.winfo_reqwidth()/2)
        y = (self.height / 2) - (self.home_screen.winfo_reqheight() / 2)
        self.home_screen.place(x=x, y=y)
        self.update_idle_timer()
        self.check_for_updates()
        self.mouse_hide_timer_id = None
        self.show_mouse()
        self.bind_all("<Motion>", self.show_mouse)

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
        self.after(config["Idle Update"], self.update_idle_timer)

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
        self.after(config["Update Delay"], self.check_for_updates)

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
