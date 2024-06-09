import tkinter as tk

from tkinter import messagebox


class UserSlice:
    def __init__(self, frame, root_window, width, user_data):
        self.root = frame
        self.root_window = root_window

        self.user_win = None

        self.user = user_data
        self.db = self.root_window.launcher.database

        self.width = width
        self.height = 50

        self.frame = None

        self.bg = self.root_window.main_bg
        self.s_bg = self.root_window.second_bg
        self.t_bg = self.root_window.third_bg
        self.fg = self.root_window.fg

    def get_name(self) -> str:
        name = self.user["name"] + " | " + self.user["preferred_name"]
        return name

    def attempt_delete(self) -> None:
        result = messagebox.askyesno("Confirmation", "Are you sure you want to "
                                                     f"proceed with deleting {self.user["name"]}?")
        if result:
            self.db.remove_user(self.user["name"])
            self.user_win.destroy()
            self.root_window.set_section(self.root_window.section)

    def user_win_config(self, win) -> None:
        win.resizable(False, False)
        win.geometry("800x550")
        win.title(self.user["name"] + " | Control Panel")
        win.config(bg=self.t_bg)

    def manage_user(self) -> None:
        self.user_win = tk.Toplevel(self.root_window.root)
        self.user_win_config(self.user_win)

        name_title = tk.Label(self.user_win, text=self.user["name"], font=("Montserrat", 30, "bold"))
        name_title.config(bg=self.t_bg, fg=self.fg)
        name_title.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=8)

        content_frame = tk.Frame(self.user_win)
        content_frame.config(bg=self.bg, highlightthickness=2, highlightbackground=self.fg)
        content_frame.place(x=-2, y=70, width=804, height=483)

        delete_account_button = tk.Button(content_frame, text="Delete User",
                                          command=self.attempt_delete)
        delete_account_button.config(bg=self.bg, fg=self.fg,
                                     font=("Montserrat", 14, "bold"), activebackground="#f0f",
                                     activeforeground=self.fg, highlightcolor=self.bg)
        delete_account_button.pack(pady=5, side=tk.RIGHT, anchor=tk.NE, padx=5)
        delete_account_button.bind("<Enter>", lambda event: delete_account_button.config(bg="#e31464"))
        delete_account_button.bind("<Leave>", lambda event: delete_account_button.config(bg=self.bg))

        user_info_sets = [
            ("Name: ", self.user["name"]),
            ("Preferred Name: ", self.user["preferred_name"]),
            ("Password: ", self.user["password"]),
            ("User Since: ", self.user["date_created"]),
            ("Last login: ", self.user["last_login"])
        ]
        for user_set in user_info_sets:
            info = tk.Label(content_frame, text=f"{user_set[0]}{user_set[1]}",
                            font=("Montserrat", 20), wraplength=780)
            info.config(bg=self.bg, fg=self.fg)
            info.pack(anchor=tk.NW, padx=10, pady=12)

    def activate(self) -> None:
        self.frame = tk.Frame(self.root, height=self.height, width=1)
        self.frame.config(bg=self.t_bg)

        name = self.get_name()
        user_name = tk.Label(self.frame, text=name, font=("Montserrat", 15))
        user_name.config(bg=self.t_bg, fg=self.fg)
        user_name.pack(pady=2, side=tk.LEFT, padx=4)

        manage_button = tk.Button(self.frame, text="Manage", command=self.manage_user)
        manage_button.config(bg=self.bg, fg=self.fg,
                             font=("Montserrat", 13), activebackground="#f0f",
                             activeforeground=self.fg, highlightcolor=self.bg)
        manage_button.pack(pady=2, side=tk.RIGHT, padx=4)
        manage_button.bind("<Enter>", lambda event: manage_button.config(bg=self.t_bg))
        manage_button.bind("<Leave>", lambda event: manage_button.config(bg=self.bg))

        self.frame.pack(fill=tk.X, pady=2)
