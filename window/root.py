import sys

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
        self.second_bg = self.color["second_bg"]
        self.third_bg = self.color["third_bg"]

        self.fg = self.color["foreground"]
        self.ag = self.color["active_ground"]
        self.border = self.color["border_color"]

        self.sc = self.color["stock_color"]
        self.gc = self.color["grid_color"]

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
        self.recursive_save()
        self.taskbar = taskbar.Taskbar(self.root, self)

        self.taskbar.clear()
        self.taskbar.place()
        self.set_section(Sect(self.root, self, self.main_bg, self.fg))
        if self.section:
            self.section.place()
        if not self.logged_in:
            self.login_screen.activate()
            self.logged_in = True
        self.recursive_save()

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
        self.sc = palette["stock_color"]
        self.gc = palette["grid_color"]

    def set_binds(self):
        def reset_color():
            self.set_palette(self.def_color)
            self.layout()
            if self.launcher.user_data is None:
                self.login_screen.activate()

        self.root.bind("<Escape>", lambda x: self.exit())
        self.root.bind('<Shift-Control-Key-R>', lambda x: reset_color())

        def on_primary_close():
            self.recursive_save()
            try:
                self.root.event_generate("<<RootDestroy>>")
                self.root.destroy()
            except Exception as e:
                print("Failed to execute on primary close because:", e)
                sys.exit()

        self.root.protocol("WM_DELETE_WINDOW", on_primary_close)

    def recursive_save(self):
        if self.launcher.user is None or self.launcher.false_account:
            return
        self.launcher.save_file()
        self.root.after(4000, self.recursive_save)

    def launch(self):
        self.root.mainloop()

    def exit(self):
        self.root.destroy()
