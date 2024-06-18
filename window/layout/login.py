import tkinter as tk
from tkinter import messagebox


class LoginScreen:
    def __init__(self, root, root_window, launcher):
        self.launcher = launcher

        self.db = self.launcher.database

        self.root = root
        self.root_window = root_window

        self.frame = tk.Frame(self.root)

        self.bg = self.root_window.main_bg
        self.s_bg = self.root_window.second_bg
        self.t_bg = self.root_window.third_bg
        self.fg = self.root_window.fg
        self.ag = self.root_window.ag

        self.width = self.root_window.size[0]
        self.height = self.root_window.size[1]

    def place(self):
        self.frame.lift()
        self.frame.place(x=0, y=0, width=self.root_window.size[0], height=self.root_window.size[1])

    def exit(self):
        self.frame.destroy()
        self.root_window.layout()
        self.root.unbind("<Control-Key-s>")
        self.root.unbind("<Control-KeyRelease-s>")

    def activate_login(self, attempt_login):
        login_frame = tk.Frame(self.frame)
        login_frame.config(bg=self.s_bg, borderwidth=1, relief=tk.SOLID)
        login_frame.place(x=self.width / 2, width=self.width / 2, y=100, height=self.height - 100)

        name_title = tk.Label(login_frame, text="Name")
        name_title.config(bg=self.s_bg, fg=self.fg, font=("Montserrat", 21, "bold"))
        name_title.pack(pady=20)
        name_box = tk.Entry(login_frame)
        name_box.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 21), justify='center', insertbackground=self.fg)
        name_box.place(x=(self.width / 2) / 2 - 175, y=55, width=350, height=50)

        password_title = tk.Label(login_frame, text="Password")
        password_title.config(bg=self.s_bg, fg=self.fg, font=("Montserrat", 21, "bold"))
        password_title.pack(pady=150.5)
        password_box = tk.Entry(login_frame)
        password_box.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 21), justify='center',
                            insertbackground=self.fg, show="*")
        password_box.place(x=(self.width / 2) / 2 - 175, y=265, width=350, height=50)
        self.root.bind("<Control-Key-s>", lambda x: password_box.config(show=""))
        self.root.bind("<Control-KeyRelease-s>", lambda x: password_box.config(show="*"))

        login_button = tk.Button(login_frame, text="Login",
                                 command=lambda: attempt_login(name_box.get(), password_box.get()))
        login_button.config(width=17, bg=self.t_bg, fg=self.fg,
                            font=("Montserrat", 24, "bold"), activebackground=self.root_window.ag,
                            activeforeground=self.fg, highlightcolor=self.t_bg)
        login_button.bind("<Enter>", lambda event: login_button.config(bg=self.bg))
        login_button.bind("<Leave>", lambda event: login_button.config(bg=self.t_bg))
        login_button.pack(pady=25)

        def cycle_focus(*args):
            if name_box.get() == "" or name_box.get() is None:
                name_box.focus()
            elif password_box.get() == "" or password_box.get() is None:
                password_box.focus()
            else:
                login_button.invoke()

        self.root.bind('<Return>', cycle_focus)

    def activate_account_request(self):
        def send_request(name, preferred_name, password, explanation):
            self.db = self.launcher.update_database()
            if self.db:
                if name.strip() and preferred_name.strip() and password.strip() and explanation.strip():
                    self.db.add_request(name.strip(), preferred_name.strip(), password.strip(), explanation.strip())
                    self.root_window.popup.activate("Your request will soon be reviewed by an admin, and you may"
                                                    " or may not get an account with the credentials provided."
                                                    " Please be patient in the meantime. Thank you!")
                else:
                    self.root_window.popup.activate("One of the boxes was left empty, or is invalid. Please fill them"
                                                    " all out correctly, with real characters. Your request will soon"
                                                    " be reviewed by an admin, and then you may or may not get an"
                                                    " account with the details you have put"
                                                    " in. Thank you for your patience.",
                                                    fontsize=13)
            else:
                messagebox.showinfo("Connections Alert",
                                    "Connections are is still loading. Wait a couple more seconds.")

        create_frame = tk.Frame(self.frame)
        create_frame.config(bg=self.s_bg, borderwidth=1, relief=tk.SOLID)
        create_frame.place(x=0, width=self.width / 2, y=100, height=self.height + 100)

        entries = [
            ["Name", None],
            ["Preferred Name", None],
            ["Password Name", None]
        ]

        tk.Frame(create_frame, bg=self.s_bg).pack(pady=7)
        for i in range(len(entries)):
            label = tk.Label(create_frame, text=entries[i][0])
            label.config(bg=self.s_bg, fg=self.fg, font=("Montserrat", 22, "bold"))
            label.pack(pady=0)
            ent = tk.Entry(create_frame)
            ent.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 21), justify='center', insertbackground=self.fg)
            entries[i][1] = ent
            ent.pack()
            tk.Frame(create_frame, bg=self.s_bg).pack(pady=14)

        reason_label = tk.Label(create_frame, text="Reason for Account")
        reason_label.config(bg=self.s_bg, fg=self.fg, font=("Montserrat", 22, "bold"))
        reason_label.place(y=320, x=50, width=self.width / 2 - 100, height=40)
        reason_text = tk.Text(create_frame)
        reason_text.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 16), insertbackground=self.fg)
        reason_text.place(x=50, y=362, width=self.width / 2 - 100, height=115)

        send_button = tk.Button(create_frame, text="Send Request",
                                command=lambda: send_request(entries[0][1].get().strip(),
                                                             entries[1][1].get().strip(),
                                                             entries[2][1].get().strip(),
                                                             reason_text.get("1.0", tk.END).strip()))
        send_button.config(width=17, bg=self.t_bg, fg=self.fg,
                           font=("Montserrat", 24, "bold"), activebackground=self.ag,
                           activeforeground=self.fg, highlightcolor=self.t_bg)
        send_button.bind("<Enter>", lambda event: send_button.config(bg=self.bg))
        send_button.bind("<Leave>", lambda event: send_button.config(bg=self.t_bg))
        send_button.pack(pady=175)

    def activate(self):
        self.launcher.user_data = None
        self.frame = tk.Frame(self.root)

        def attempt_login(name, password):
            self.db = self.launcher.update_database()
            if self.db:
                if self.db.login_check(name, password):
                    self.launcher.user_data = self.db.get_data(name)
                    self.db.update_last_date(name)
                    self.db.set_user_data(name, self.root_window.def_color)
                    self.root_window.set_palette(self.db.get_color_palette(name))
                    self.root.unbind("<Return>")
                    self.exit()
                else:
                    self.root_window.popup.activate("Login incorrect. Try checking spelling, and cases. Both the name "
                                                    "and password are space and case sensitive. If you forget your "
                                                    "password, contact an admin.")
            else:
                messagebox.showinfo("Connections Alert",
                                    "Connections are is still loading. Wait a couple more seconds.")

        self.frame.config(bg=self.bg)

        title = tk.Label(self.frame, text=f"Login to {self.launcher.name}")
        title.config(bg=self.bg, fg=self.fg, font=("Montserrat", 32, "bold"))
        title.pack(pady=19)

        version = tk.Label(self.frame, text=f"Version {self.root_window.launcher.version}", font=("Montserrat", 10))
        version.config(fg=self.fg, bg=self.bg)
        version.place(x=3, y=3, height=20, width=80)

        self.activate_login(attempt_login)

        self.activate_account_request()

        self.place()
