import window.utils.color as uc

import tkinter as tk


class Section:
    def __init__(self, root, root_window, bg, fg):
        self.root = root
        self.root_window = root_window

        self.bg = bg
        self.fg = fg

        self.frame = tk.Frame()
        self.frame.config(bg=self.bg)

    def place(self):
        self.frame.place(x=self.root_window.taskbar.width, y=0,
                         width=self.root_window.size[0] - self.root_window.taskbar.width,
                         height=self.root_window.size[1])

    def activate(self):
        self.place()

    def hide(self):
        for child in self.frame.winfo_children():
            child.destroy()

        self.frame.place(y=-100000)
