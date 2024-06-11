import window.utils.color as uc
import window.utils.popup as up

import window.layout.login as login
import window.layout.taskbar as taskbar
from window.layout.section import Section as Sect

import tkinter as tk


class RootWindow:
    def __init__(self, launcher):
        # Window Data
        self.root = tk.Tk()
        self.size = (1100, 700)

        self.launcher = launcher

        self.main_bg = uc.rgb_to_hex(55, 79, 78)
        self.second_bg = uc.rgb_to_hex(45, 69, 68)
        self.third_bg = uc.rgb_to_hex(76, 115, 113)

        self.fg = uc.rgb_to_hex(245, 250, 250)

        print(f"FG={self.fg}\nBG={self.main_bg}\nBG2={self.second_bg}\nBG3={self.third_bg}")

        self.popup = up.Popup(self.root, self)

        # Layout Objects
        self.login_screen = login.LoginScreen(self.root, self, self.launcher)
        self.logged_in = False

        self.taskbar = taskbar.Taskbar(self.root, self)
        self.section = None

    def init_root_data(self):
        self.root.title(f"{self.launcher.name}")
        self.root.resizable(False, False)
        self.root.geometry(f"{self.size[0]}x{self.size[1]}")
        self.root.maxsize(*self.size)
        self.root.config(bg=self.main_bg)
        self.root.iconbitmap('favicon.ico')

    def layout(self):
        self.taskbar.clear()
        self.taskbar.place()
        self.set_section(Sect(self.root, self, self.main_bg, self.fg))
        if self.section:
            self.section.place()
        if not self.logged_in:
            self.login_screen.activate()
            self.logged_in = True

    def set_section(self, section):
        if self.section:
            self.section.hide()
        self.section = section
        self.section.activate()

    def set_binds(self):
        self.root.bind("<Escape>", lambda x: self.exit())

    def launch(self):
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
