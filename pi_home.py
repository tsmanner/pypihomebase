#! python3

import common
import config
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
        self.settings = config.Configuration()
        self.focus_set()
        self.bind_all("<Escape>", lambda e: e.widget.quit())
        self.wm_title("Raspberry Pi Home Base")
        self.config(bg="dark gray")
        self.config(cursor="left_ptr")
        # Member initialization
        self.idle_screen = None
        self.idle_delay = self.settings["Idle Delay"]
        self.mouse_hide_timer_id = None
        self.screens = {}
        self.timed_events = {}
        # Setup base funcitonality for idle and mouse visibility
        self.check_for_updates()
        self.show_mouse()
        self.bind_all("<Motion>", self.show_mouse)
        # Build all the screens from the config file
        [self.add_screen(screen, self.settings["Screens"][screen]) for screen in self.settings["Screens"]]
        [self.add_event(event, self.settings["Timed Events"][event]) for event in self.settings["Timed Events"]]
        self.current_screen = self.screens[self.settings["Boot Screen"]]
        self.update_idletasks()
        x = (self.width/2) - (self.current_screen.winfo_reqwidth()/2)
        y = (self.height / 2) - (self.current_screen.winfo_reqheight() / 2)
        self.current_screen.place(x=x, y=y)

    def add_screen(self, screen_name, screen_data):
        screen = pi_screen.Screen(self, screen_name, screen_data)
        self.screens[screen_name] = screen

    def every(self, ms, func=None, *args):
        if func:
            func(*args)
            self.after(ms, self.every, ms, func, *args)

    def add_event(self, event, event_data):
        try:
            module = event_data["command"]["module"]
            function = event_data["command"]["function"]
            if module != "":
                exec("import %s" % module)
                command = eval("%s.%s" % (module, function))
            else:
                command = eval("%s" % function)
            event_data["command"] = command
        except KeyError:
            print(event_data)
            raise KeyError("No command specified for timed event!")
        self.every(event_data["time"], command)
        self.timed_events[event] = event_data

    def screen_lock(self):
        if self.idle_delay == self.settings["Idle Delay"]:
            self.idle_delay = self.settings["Locked Delay"]
        else:
            self.idle_delay = self.settings["Idle Delay"]

    def update_idle_timer(self, event=None):
        # Check the time and see if we should go idle, if not update the time again
        if self.idle_screen:
            if common.idle() < self.idle_delay:
                self.do_home_screen()
        else:
            if common.idle() >= self.idle_delay:
                self.do_idle_screen()

    def do_idle_screen(self, event=None):
        self.idle_delay = self.settings["Idle Delay"]
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
        self.config(cursor=self.settings["Cursor"])
        self.mouse_hide_timer_id = self.after(self.settings["Mouse Hide Delay"], self.hide_mouse)


if __name__ == "__main__":
    home = HomeGui()
    home.mainloop()
