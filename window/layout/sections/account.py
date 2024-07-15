from window.layout.section import Section

import tkinter as tk
from tkinter import colorchooser

from window.utils.color import hex_color_brightness as hcb


class AccountSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.user = self.root_window.launcher.user_data
        self.color = self.root_window.color

    def bind_password_show(self, password):
        def no_show(*args):
            password.config(text="Password: {}".format("*" * len(self.user["password"])))

        def show(*args):
            password.config(text="Password: {}".format(self.user["password"]))

        self.root.bind("<Control-Key-s>", show)
        self.root.bind("<KeyRelease-s>", no_show)

    def show_info(self):
        name = tk.Label(self.frame, text=f"{self.user["name"]} | {self.user["preferred_name"]}",
                        font=("Montserrat", 32, "bold"))
        name.config(bg=self.color["main_bg"], fg=self.color["foreground"])
        name.pack(side=tk.TOP, anchor=tk.W, padx=2)

        password = tk.Label(self.frame, text=f"Password: {"*" * len(self.user["password"])}")
        password.config(bg=self.color["main_bg"], fg=self.color["foreground"], font=("Montserrat", 20))
        password.pack(side=tk.TOP, anchor=tk.W, padx=50, pady=20)
        self.bind_password_show(password)

        info_sets = {
            ("Last Login: ", self.user["last_login"]),
            ("Date Joined: ", self.user["date_created"]),
        }
        for s in info_sets:
            label = tk.Label(self.frame, text=f"{s[0]}{s[1]}", font=("Montserrat", 20))
            label.config(bg=self.color["main_bg"], fg=self.color["foreground"])
            label.pack(side=tk.TOP, anchor=tk.W, padx=50, pady=20)

        preferences = tk.Label(self.frame, text="Color Preferences",
                               font=("Montserrat", 32, "bold"))
        preferences.config(bg=self.color["main_bg"], fg=self.color["foreground"])
        preferences.pack(side=tk.TOP, anchor=tk.W, padx=2)

        color_changer_sets = {
            "Background 1": "main_bg",
            "Background 2": "second_bg",
            "Background 3": "third_bg",
            "Foreground": "foreground",
            "Grid Color": "grid_color",
            "Stock Color": "stock_color",
            "Active Color": "active_ground",
            "Border Color": "border_color"
        }
        color_copy = self.color.copy()
        colors_frame = tk.Frame(self.frame, bg=self.color["main_bg"])
        colors_frame.place(x=50, y=350, height=600, width=275)
        col_left = tk.Frame(colors_frame, width=200, bg=self.color["main_bg"])
        col_left.place(y=0, x=0, width=115, height=600)
        col_right = tk.Frame(colors_frame, width=200, bg=self.color["main_bg"])
        col_right.place(y=0, x=160, width=115, height=600)
        for i, color_set in enumerate(color_changer_sets):
            def change_color(k):
                new = colorchooser.askcolor(initialcolor=color_copy[k])[1]
                if new is not None:
                    color_copy[k] = new
                    self.root_window.set_palette(color_copy)
                    self.root_window.layout()
                    self.root_window.set_section(AccountSection(self.root, self.root_window))

            e = i % 2 == 1
            key = color_changer_sets[color_set]
            bright = hcb(self.color[key])
            button = tk.Button(col_left if e else col_right, text=color_set, font=("Montserrat", 12),
                               command=lambda k=key: change_color(k), width=80)
            button.config(activebackground=self.color["active_ground"], bg=self.color[key],
                          fg="black" if bright >= 400 else "white")
            button.pack(side=tk.TOP, anchor=tk.W if e else tk.E, pady=10, fill=tk.X)

        save_colors = tk.Button(self.frame, text="Save Colors", command=lambda: self.root_window.launcher.database.
                                set_color_palette(self.user["name"], self.root_window.color))
        save_colors.config(bg=self.color["third_bg"], activebackground=self.color["active_ground"],
                           font=("Montserrat", 13, "bold"), fg=self.color["foreground"])
        save_colors.bind("<Enter>", lambda x: save_colors.config(bg=self.color["second_bg"]))
        save_colors.bind("<Leave>", lambda x: save_colors.config(bg=self.color["third_bg"]))
        save_colors.place(x=50, y=600, width=110, height=40)

        def reset_colors():
            self.root_window.set_palette(self.root_window.def_color)
            self.root_window.layout()
            self.root_window.set_section(AccountSection(self.root, self.root_window))
        reset_colors = tk.Button(self.frame, text="Reset",
                                 command=reset_colors)
        reset_colors.config(bg=self.color["third_bg"], activebackground=self.color["active_ground"],
                            font=("Montserrat", 13, "bold"), fg=self.color["foreground"])
        reset_colors.bind("<Enter>", lambda x: reset_colors.config(bg=self.color["second_bg"]))
        reset_colors.bind("<Leave>", lambda x: reset_colors.config(bg=self.color["third_bg"]))
        reset_colors.place(x=215, y=600, width=110, height=40)

    def activate(self):
        print(self.root_window.launcher.user_stock)
        self.show_info()

        super().place()

    def hide(self):
        self.root.unbind("<Control-Key-s>")
        self.root.unbind("<KeyRelease-s>")

        super().hide()
