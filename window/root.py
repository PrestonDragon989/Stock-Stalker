import window.utils.color as uc
import window.utils.popup as up

import window.layout.login as login
import window.layout.taskbar as taskbar
from window.layout.section import Section as Sect

import tkinter as tk


class RootWindow:
    def __init__(self, launcher):
        self.launcher = launcher

        # Window Data
        self.root = tk.Tk()
        self.size = (1100, 700)

        # Color Palette
        self.def_color = uc.color_palette.copy()
        self.color = uc.color_palette

        self.main_bg = self.color["main_bg"]
        self.second_bg = uc.rgb_to_hex(45, 69, 68)
        self.third_bg = uc.rgb_to_hex(76, 115, 113)

        self.fg = uc.rgb_to_hex(245, 250, 250)
        self.ag = uc.rgb_to_hex(255, 0, 255)
        self.border = uc.rgb_to_hex(0, 0, 255)

        self.stock_up = uc.rgb_to_hex(51, 255, 58)
        self.stock_down = uc.rgb_to_hex(255, 51, 51)

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
        self.taskbar = taskbar.Taskbar(self.root, self)

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

    def set_palette(self, palette):
        self.color = palette
        self.main_bg = palette["main_bg"]
        self.second_bg = palette["second_bg"]
        self.third_bg = palette["third_bg"]
        self.fg = palette["foreground"]
        self.ag = palette["active_ground"]
        self.border = palette["border_color"]
        self.stock_up = palette["stock_up"]
        self.stock_down = palette["stock_down"]

    def set_binds(self):
        def reset_color():
            self.set_palette(self.def_color)
            self.layout()
            if self.launcher.user_data is None:
                self.login_screen.activate()
        self.root.bind("<Escape>", lambda x: self.exit())
        self.root.bind('<Shift-Control-Key-R>', lambda x: reset_color())

    def launch(self):
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
