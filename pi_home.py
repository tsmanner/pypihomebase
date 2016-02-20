#! python3

import idle
import pi_screen
import tkinter as tk

IDLE_UPDATE = 10
DEFAULT_TIMER = 1000
LOCK_TIMER = 5000


class HomeGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        #self.attributes('-fullscreen', True)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        self.focus_set()
        self.bind_all("<Escape>", lambda e: e.widget.quit())
        self.wm_title("12 Pine Echo Home")
        self.idle_screen = None
        self.config(bg="dark gray")
        self.config(cursor="")
        self.idle_delay = DEFAULT_TIMER
        self.home_screen = pi_screen.HomeScreen(self)
        self.update_idletasks()
        x = (self.width/2) - (self.home_screen.winfo_reqwidth()/2)
        y = (self.height/2) - (self.home_screen.winfo_reqheight()/2)
        self.home_screen.place(x=x, y=y)
        self.update_idle_timer()

    def screen_lock(self):
        self.idle_delay = LOCK_TIMER

    def update_idle_timer(self, event=None):
        # Check the time and see if we should go idle, if not update the time again
        if self.idle_screen:
            if idle.idle() <= self.idle_delay:
                self.do_home_screen()
        else:
            if idle.idle() > self.idle_delay:
                self.do_idle_screen()
        self.after(IDLE_UPDATE, self.update_idle_timer)

    def do_idle_screen(self, event=None):
        self.idle_delay = DEFAULT_TIMER
        self.idle_screen = pi_screen.HomeIdleScreen(self)

    def do_home_screen(self, event=None):
        if self.idle_screen:
            self.idle_screen.destroy()
            self.idle_screen = None

if __name__ == "__main__":
    home = HomeGui()
    home.mainloop()
