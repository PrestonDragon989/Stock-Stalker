from window.layout.section import Section

from window.layout.admin_tools.user_slice import UserSlice
from window.layout.admin_tools.request_slice import RequestSlice

import tkinter as tk
from tkinter import ttk


class AdminPanelSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.db = self.root_window.launcher.database

        self.requests_frame = tk.Frame(self.frame)
        self.scrollable_requests_frames = None
        self.requests_canvas = None
        self.requests_scrollbar = None

        self.accounts_frame = tk.Frame(self.frame)
        self.scrollable_accounts_frames = None
        self.accounts_canvas = None
        self.accounts_scrollbar = None

        self.width = self.root_window.size[0] - self.root_window.taskbar.width
        self.height = self.root_window.size[1]

        self.bg = self.root_window.main_bg
        self.s_bg = self.root_window.second_bg
        self.t_bg = self.root_window.third_bg
        self.fg = self.root_window.fg

        self.scroll_style = ttk.Style()
        self.scroll_style.theme_use('classic')
        self.scroll_style.configure("Vertical.TScrollbar",
                                    gripcount=0,
                                    lightcolor=self.bg,
                                    darkcolor=self.bg,
                                    background=self.t_bg,
                                    troughcolor=self.s_bg,
                                    bordercolor=self.root_window.border,
                                    arrowcolor=self.t_bg)

    def bind_widgets_scroll(self, widget, canvas):
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))
        for child in widget.winfo_children():
            self.bind_widgets_scroll(child, canvas)

    def set_frames(self):
        self.requests_frame = tk.Frame(self.frame)
        self.accounts_frame = tk.Frame(self.frame)

        # Requests frame
        self.requests_frame.config(bg=self.s_bg, highlightthickness=2, highlightbackground=self.root_window.border)
        self.requests_frame.place(x=-1, y=100, width=self.width / 2, height=self.height - 100)
        self.requests_canvas = tk.Canvas(self.requests_frame)
        self.requests_canvas.config(bg=self.s_bg, highlightthickness=2, highlightbackground=self.s_bg)
        self.requests_scrollbar = ttk.Scrollbar(self.requests_frame, orient="vertical",
                                                command=self.requests_canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_requests_frames = tk.Frame(self.requests_canvas)
        self.scrollable_requests_frames.config(bg=self.s_bg)
        self.scrollable_requests_frames.bind("<Configure>", lambda e: self.requests_canvas.configure(
            scrollregion=self.requests_canvas.bbox("all")))

        self.requests_canvas.configure(yscrollcommand=self.requests_scrollbar.set)
        self.requests_canvas.create_window((0, 0), window=self.scrollable_requests_frames, anchor="nw", width=430)
        self.requests_canvas.pack(side="right", fill="both", expand=True)
        self.requests_scrollbar.pack(side="left", fill="y")

        # Account Frame
        self.accounts_frame.config(bg=self.bg, highlightthickness=2, highlightbackground=self.root_window.border)
        self.accounts_frame.place(x=self.width / 2 - 1, y=100, width=self.width / 2 + 1, height=self.height - 100)
        self.accounts_canvas = tk.Canvas(self.accounts_frame)
        self.accounts_canvas.config(bg=self.s_bg, highlightthickness=2, highlightbackground=self.s_bg)
        self.accounts_scrollbar = ttk.Scrollbar(self.accounts_frame, orient="vertical",
                                                command=self.accounts_canvas.yview, style="Vertical.TScrollbar")
        self.scrollable_accounts_frames = tk.Frame(self.accounts_canvas)
        self.scrollable_accounts_frames.config(bg=self.s_bg)
        self.scrollable_accounts_frames.bind("<Configure>", lambda e: self.accounts_canvas.configure(
            scrollregion=self.accounts_canvas.bbox("all")))

        self.accounts_canvas.create_window((0, 0), window=self.scrollable_accounts_frames, anchor="nw", width=430)
        self.accounts_canvas.configure(yscrollcommand=self.accounts_scrollbar.set)
        self.accounts_canvas.pack(side="right", fill="both", expand=True)
        self.accounts_scrollbar.pack(side="left", fill="y")

    def set_slices(self):
        for user in self.db.user_data.find():
            UserSlice(self.scrollable_accounts_frames, self.root_window,
                      1000, user).activate()

        for request in self.db.request_data.find():
            RequestSlice(self.scrollable_requests_frames, self.root_window,
                         1000, request).activate()

    def activate(self):
        self.set_frames()

        title = tk.Label(self.frame, text="Admin Panel")
        title.config(font=("Montserrat", 32, "bold"), bg=self.bg, fg=self.fg)
        title.pack(pady=20)

        self.set_slices()

        self.bind_widgets_scroll(self.accounts_frame, self.accounts_canvas)
        self.bind_widgets_scroll(self.requests_frame, self.requests_canvas)

        super().place()
