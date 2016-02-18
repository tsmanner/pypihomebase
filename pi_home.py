#! python3

import pi_idle
import tkinter as tk


class Layer(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.visible = False

    def pack(self, *args, **kwargs):
        tk.Frame.pack(self, *args, **kwargs)
        self.visible = True

    def pack_forget(self):
        tk.Frame.pack_forget(self)
        self.visible = False


class HomeScreen(Layer):
    def __init__(self, master):
        Layer.__init__(self, master, width=800, height=400)
        self.box1 = tk.LabelFrame(self, text="BOX 1", width=400, height=400)
        self.box1.pack(side=tk.LEFT)
        self.box2 = tk.LabelFrame(self, text="BOX 2", width=400, height=400)
        self.box2.pack(side=tk.LEFT)


class HomeGui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(width=800, height=400)
        self.wm_title("12 Pine Echo Home")
        self.swap_button = tk.Button(self, text="Swap", bg="black", fg="dark orange", command=self.swap)
        self.swap_button.pack(side=tk.TOP, fill=tk.X)
        self.idle_screen = pi_idle.HomeIdleScreen(self)
        self.idle_screen.pack(fill=tk.BOTH)
        self.home_screen = HomeScreen(self)
        self.idle_timer_id = None
        self.bind("*", self.set_idle_timer)
        self.set_idle_timer()

    def set_idle_timer(self):
        self.idle_timer_id = self.after(5000, self.swap, "idle")

    def swap(self, reason="swap", event=None):
        print("In swap", reason)
        if self.idle_screen.visible:
            if reason == "idle":
                return
            self.idle_screen.pack_forget()
            self.swap_button.config(bg="white", fg="black")
            self.home_screen.pack(fill=tk.BOTH)
            self.idle_timer_id = self.after(5000, self.swap, "idle")
        elif self.home_screen.visible:
            self.home_screen.pack_forget()
            self.swap_button.config(bg="black", fg="dark orange")
            self.idle_screen.pack(fill=tk.BOTH)
            if self.idle_timer_id:
                self.after_cancel(self.idle_timer_id)
                self.idle_timer_id = None

if __name__ == "__main__":
    home = HomeGui()
    home.mainloop()
