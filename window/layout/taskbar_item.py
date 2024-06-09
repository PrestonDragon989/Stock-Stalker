import tkinter as tk


class TaskbarItem:
    def __init__(self, main_bg, second_bg, fg, text, section, width_cap, section_setter, modified=False):
        self.main_bg = main_bg
        self.second_bg = second_bg
        self.fg = fg

        self.text = text
        self.section = section

        self.width_cap = width_cap
        self.base_height = 50

        self.frame = None

        self.section_setter = section_setter

        self.modified = modified

    def enter(self, *args):
        self.frame.config(bg=self.second_bg)
        for child in self.frame.winfo_children():
            child.config(bg=self.second_bg)

    def leave(self, *args):
        self.frame.config(bg=self.main_bg)
        for child in self.frame.winfo_children():
            child.config(bg=self.main_bg)

    def click(self, *args):
        if not self.modified:
            self.frame.config(bg="#f0f")
            for child in self.frame.winfo_children():
                child.config(bg="#f0f")
            self.section_setter(self.section)
        if self.modified:
            self.frame.config(bg="#f0f")
            for child in self.frame.winfo_children():
                child.config(bg="#f0f")
            self.section_setter()

    def config_frame(self, frame, y):
        self.frame = tk.Frame(frame, borderwidth=1, relief=tk.SOLID)

        text = tk.Label(self.frame, bg=self.main_bg, fg=self.fg, text=self.text, font=("Montserrat", 14, "bold"))
        text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.frame.config(bg=self.main_bg, height=self.base_height, highlightbackground=self.fg)

        self.frame.bind("<Enter>", self.enter)
        self.frame.bind("<Leave>", self.leave)
        self.frame.bind("<Button-1>", self.click)
        for child in self.frame.winfo_children():
            child.bind("<Enter>", self.enter)
            child.bind("<Leave>", self.leave)
            child.bind("<Button-1>", self.click)

        self.frame.place(x=-1, y=y, width=self.width_cap, height=self.base_height)
