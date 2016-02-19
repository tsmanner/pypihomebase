#! python3

import pi_screen
import tkinter as tk


class HomeGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-fullscreen', True)
#        self.overrideredirect(1)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
#        self.geometry("%dx%d+%d+%d" % (self.width, self.height, 0, 0))
        self.focus_set()
        self.bind_all("<Escape>", lambda e: e.widget.quit())
        self.wm_title("12 Pine Echo Home")
        self.idle_screen = pi_screen.HomeIdleScreen(self)
        self.home_screen = pi_screen.HomeScreen(self)
        self.idle_timer_id = None
        self.bind_all("<Key>", self.set_idle_timer)
        self.bind_all("<Button>", self.set_idle_timer)
        self.bind_all("<Motion>", self.set_idle_timer)
        self.do_home_screen()

    def set_idle_timer(self, event=None):
        if self.idle_timer_id:
            self.after_cancel(self.idle_timer_id)
        self.idle_timer_id = self.after(1000, self.do_idle_screen)
        if self.idle_screen.visible:
            self.do_home_screen()

    def do_idle_screen(self, event=None):
        self.home_screen.pack_forget()
        x = (self.width/2) - (self.idle_screen.time.winfo_reqwidth()/2)
        y = (self.height/2) - (self.idle_screen.time.winfo_reqheight()/2)
        self.idle_screen.place(x=x, y=y)
        self.config(bg="black")
        self.config(cursor="none")

    def do_home_screen(self, event=None):
        self.idle_screen.place_forget()
        self.home_screen.pack()
        self.config(bg="dark gray")
        self.set_idle_timer()
        self.config(cursor="")

if __name__ == "__main__":
    home = HomeGui()
    home.mainloop()
