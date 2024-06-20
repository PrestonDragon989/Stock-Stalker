from window.layout.section import Section

import tkinter as tk

from window.utils.website import OpenSite


class WelcomeSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.user = self.root_window.launcher.user_data

        self.color = self.root_window.color

        self.site = OpenSite()

    def activate(self):
        title = tk.Label(self.frame, text=f"Welcome, {self.user["preferred_name"]}!", font=("Montserrat", 32, "bold"))
        title.config(bg=self.bg, fg=self.fg)
        title.pack(pady=6)

        super().place()
