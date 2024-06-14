import tkinter as tk
from tkinter import messagebox


class RequestSlice:
    def __init__(self, frame, root_window, width, request_data) -> None:
        self.root = frame
        self.root_window = root_window

        self.bg = self.root_window.main_bg
        self.s_bg = self.root_window.second_bg
        self.t_bg = self.root_window.third_bg
        self.fg = self.root_window.fg
        self.ag = self.root_window.ag

        self.width = width
        self.height = 50

        self.request = request_data
        self.db = self.root_window.launcher.database

        self.frame = None

        self.view_win = None

    def get_name(self) -> str:
        return self.request["name"] + " | " + self.request["preferred_name"]

    def decline_request(self) -> None:
        result = messagebox.askyesno("Confirmation", "Are you sure you want to "
                                                     f"proceed with declining {self.request["name"]}?")
        if result:
            self.db.remove_request(self.request["name"])
            if self.view_win:
                self.view_win.destroy()
            self.root_window.set_section(self.root_window.section)

    def accept_request(self) -> None:
        result = messagebox.askyesno("Confirmation", "Are you sure you want to "
                                                     f"proceed with accepting {self.request["name"]}?")
        if result:
            self.db.add_user(self.request["name"], self.request["preferred_name"], self.request["password"], 1)
            self.db.remove_request(self.request["name"])
            if self.view_win:
                self.view_win.destroy()
            self.root_window.set_section(self.root_window.section)

    def request_win_config(self, win) -> None:
        win.resizable(False, False)
        win.geometry("800x550")
        win.title(self.request["name"] + " | Account Request Review")
        win.config(bg=self.t_bg)

    def view_request(self):
        self.view_win = tk.Toplevel(self.root_window.root)
        self.request_win_config(self.view_win)

        name_title = tk.Label(self.view_win, text=self.request["name"], font=("Montserrat", 30, "bold"))
        name_title.config(bg=self.t_bg, fg=self.fg)
        name_title.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=8)

        content_frame = tk.Frame(self.view_win)
        content_frame.config(bg=self.bg, highlightthickness=2, highlightbackground=self.fg)
        content_frame.place(x=-2, y=70, width=804, height=483)

        request_info_sets = [
            ("Name: ", self.request["name"]),
            ("Preferred Name: ", self.request["preferred_name"]),
            ("Password: ", self.request["password"]),
            ("Date Asked: ", self.request["date"]),
            ("Request Explanation: ", "")
        ]
        for request_info in request_info_sets:
            info = tk.Label(content_frame, text=f"{request_info[0]}{request_info[1]}",
                            font=("Montserrat", 20), wraplength=780)
            info.config(bg=self.bg, fg=self.fg)
            info.pack(anchor=tk.NW, padx=10, pady=12)
        explanation = tk.Label(content_frame, text=f"\"{self.request["explanation"]}\"", wraplength=820)
        explanation.config(font=("Montserrat", 15, "italic"), fg=self.fg, bg=self.bg)
        explanation.pack(anchor=tk.NW, padx=40, pady=10)

        accept_button = tk.Button(content_frame, text="Accept", command=self.accept_request)
        accept_button.config(font=("Montserrat", 20, "bold"), fg=self.fg, bg=self.t_bg,
                             activebackground=self.ag, activeforeground=self.fg)
        accept_button.bind("<Enter>", lambda x: accept_button.config(bg=self.s_bg))
        accept_button.bind("<Leave>", lambda x: accept_button.config(bg=self.t_bg))
        accept_button.place(x=670, y=9)

        decline_button = tk.Button(content_frame, text="Decline", command=self.decline_request)
        decline_button.config(font=("Montserrat", 20, "bold"), fg=self.fg, bg=self.t_bg,
                              activebackground=self.ag, activeforeground=self.fg)
        decline_button.bind("<Enter>", lambda x: decline_button.config(bg=self.s_bg))
        decline_button.bind("<Leave>", lambda x: decline_button.config(bg=self.t_bg))
        decline_button.place(x=540, y=9)

    def activate(self) -> None:
        self.frame = tk.Frame(self.root)
        self.frame.config(bg=self.t_bg)

        name = self.get_name()
        user_name = tk.Label(self.frame, text=name, font=("Montserrat", 15))
        user_name.config(bg=self.t_bg, fg=self.fg)
        user_name.pack(pady=2, side=tk.LEFT, padx=4)

        view_button = tk.Button(self.frame, text="View", command=self.view_request)
        view_button.config(bg=self.bg, fg=self.fg,
                           font=("Montserrat", 13), activebackground=self.ag,
                           activeforeground=self.fg, highlightcolor=self.bg)
        view_button.pack(pady=2, side=tk.RIGHT, padx=6)
        view_button.bind("<Enter>", lambda event: view_button.config(bg=self.t_bg))
        view_button.bind("<Leave>", lambda event: view_button.config(bg=self.bg))

        decline_button = tk.Button(self.frame, text="Decline", command=self.decline_request)
        decline_button.config(bg=self.bg, fg=self.fg,
                              font=("Montserrat", 13), activebackground=self.ag,
                              activeforeground=self.fg, highlightcolor=self.bg)
        decline_button.pack(pady=2, side=tk.RIGHT)
        decline_button.bind("<Enter>", lambda event: decline_button.config(bg=self.t_bg))
        decline_button.bind("<Leave>", lambda event: decline_button.config(bg=self.bg))

        self.frame.pack(fill=tk.X, pady=2)
