import window.layout.taskbar_item as ti
import window.layout.section as sect

from window.layout.sections.data_src import DataSrcSection as DataSrc
from window.layout.sections.stock_searcher import StockSearcherSection as StockSearcher
from window.layout.sections.stock_keeper import StockKeeperSection as StockKeeper

from window.layout.sections.account import AccountSection

import tkinter as tk


class Taskbar:
    def __init__(self, root, root_window):
        self.root = root
        self.root_window = root_window

        self.frame = tk.Frame(root)
        self.width = 200

        self.bg = self.root_window.second_bg
        self.frame.config(bg=self.bg, highlightthickness=1, highlightcolor=self.root_window.border,
                          highlightbackground=self.root_window.border, relief=tk.SOLID)

        self.items = [
            ti.TaskbarItem(self.root_window.second_bg, self.root_window.third_bg, self.root_window.fg,
                           self.root_window.ag, "Stock Searcher",
                           StockSearcher(self.root, self.root_window), self.width,
                           self.root_window.set_section, self.root_window.border),

            ti.TaskbarItem(self.root_window.second_bg, self.root_window.third_bg, self.root_window.fg,
                           self.root_window.ag, "Stock Keeper",
                           StockKeeper(self.root, self.root_window), self.width,
                           self.root_window.set_section, self.root_window.border),

            ti.TaskbarItem(self.root_window.second_bg, self.root_window.third_bg, self.root_window.fg,
                           self.root_window.ag, "Data Src",
                           DataSrc(self.root, self.root_window), self.width,
                           self.root_window.set_section, self.root_window.border),
        ]

        self.bottom_options = [
            ti.TaskbarItem(self.root_window.second_bg, self.root_window.third_bg, self.root_window.fg,
                           self.root_window.ag, "Exit",
                           None, self.width, self.root_window.exit, self.root_window.border, modified=True),
            ti.TaskbarItem(self.root_window.second_bg, self.root_window.third_bg, self.root_window.fg,
                           self.root_window.ag, "Log out",
                           None, self.width, self.logout, self.root_window.border, modified=True),
            ti.TaskbarItem(self.root_window.second_bg, self.root_window.third_bg, self.root_window.fg,
                           self.root_window.ag, "Account",
                           AccountSection(self.root, self.root_window), self.width,
                           self.root_window.set_section, self.root_window.border),
        ]

    def logout(self):
        self.root_window.set_palette(self.root_window.def_color)
        self.root_window.login_screen.activate()

    def place(self):
        self.frame.place(x=0, y=0, width=self.width, height=self.root_window.size[1])

        self.update_items()

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def update_items(self):
        if self.root_window.launcher.false_account:
            self.bottom_options.remove(self.bottom_options[-1])

        self.frame.bind("<Button-1>", lambda event:
                        self.root_window.set_section(
                            sect.Section(self.root, self.root_window,
                                         self.root_window.main_bg,
                                         self.root_window.fg)))

        for item in range(len(self.items)):
            self.items[item].config_frame(self.frame, item * self.items[item].base_height - (item - 1) - 2)

        index = 1
        for item in self.bottom_options:
            item.config_frame(self.frame, self.root_window.size[1] -
                              (index * item.base_height + 1 - (index - 1)))
            index += 1
