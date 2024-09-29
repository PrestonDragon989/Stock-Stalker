import os.path
import tkinter as tk

from tkinter import messagebox

from window.layout.sections.welcome import WelcomeSection


class LoginScreen:
    def __init__(self, root, root_window, launcher):
        self.launcher = launcher

        self.root = root
        self.root_window = root_window
        self.controller = self.launcher.account_controller

        self.width = self.root_window.size[0]
        self.height = self.root_window.size[1]

        self.color = self.root_window.color
        self.fg = self.color["foreground"]

        self.frame = tk.Frame(self.root)

        self.login_options_frame = None
        self.login_content_frame = None

    def place(self):
        self.frame.lift()
        self.frame.place(x=0, y=0, width=self.root_window.size[0], height=self.root_window.size[1])

    def exit(self):
        self.frame.destroy()
        self.root_window.layout()
        self.root.unbind("<Control-l>")
        self.root.unbind("<Control-c>")
        self.root.unbind("<Control-p>")
        self.root_window.set_section(WelcomeSection(self.root, self.root_window))

    def create_defaults_on_frame(self):
        title = tk.Label(self.frame, text=f"Login to {self.launcher.name}")
        title.config(bg=self.color["main_bg"], fg=self.fg, font=("Montserrat", 32, "bold"))
        title.pack(pady=19)

        version = tk.Label(self.frame, text=f"Version {self.root_window.launcher.version}", font=("Montserrat", 10))
        version.config(fg=self.fg, bg=self.color["main_bg"])
        version.place(x=3, y=3, height=20, width=80)

    def clear_login_content(self):
        for widget in self.login_content_frame.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        def get_file(file=None):
            file = self.controller.get_file(None if not file else file)
            if file == 2:
                messagebox.showinfo("File Type Error", "The given file is not a .json file, or valid account"
                                                       " file.")
                for widget in login_frame.winfo_children():
                    widget.destroy()
                choose_file.delete(0, tk.END)
                choose_file.insert(0, "")
            elif type(file) is str:
                for widget in login_frame.winfo_children():
                    widget.destroy()
                file = os.path.abspath(file)
                choose_file.delete(0, tk.END)
                choose_file.insert(0, file)
                create_login_auth(file)
            else:
                choose_file.delete(0, tk.END)
                choose_file.insert(0, "")
                for widget in login_frame.winfo_children():
                    widget.destroy()

        self.clear_login_content()

        choose_file = tk.Entry(self.login_content_frame, width=300)
        choose_file.config(bg=self.color["main_bg"], fg=self.fg,
                           font=("Montserrat", 15), insertbackground=self.fg)
        choose_file.place(x=30, y=30, width=600, height=40)
        choose_file.bind("<Return>", lambda x: get_file(choose_file.get()))
        choose_file.focus_set()
        browse_file = tk.Button(self.login_content_frame, text="Browse Files", command=lambda: get_file())
        browse_file.config(bg=self.color["main_bg"], fg=self.fg, font=("Montserrat", 15), activeforeground=self.fg,
                           activebackground=self.color["main_bg"])
        browse_file.bind("<Enter>", lambda x: browse_file.config(bg=self.color["third_bg"]))
        browse_file.bind("<Leave>", lambda x: browse_file.config(bg=self.color["main_bg"]))
        browse_file.place(x=650, y=30, width=150, height=40)

        login_frame = tk.Frame(self.login_content_frame, bg=self.color["second_bg"])
        login_frame.place(x=0, y=100, width=self.width - 251, height=4910)

        def create_login_auth(file_path):
            # User Sets and Logics
            user = self.controller.get_data(file_path)

            def login_logic():
                print(user)
                if name_input.get() == user["user"]["name"] and password_input.get() == user["user"]["password"]:
                    self.launcher.set_user_data(user)
                    self.launcher.file_location = file_path
                    self.root_window.set_palette(self.launcher.user["color"])
                    self.exit()
                else:
                    messagebox.showwarning("Failed to log in", "Name or Password is incorrect. Both are "
                                                               "case sensitive. Please make sure both "
                                                               "are filled in, & correct.")

            # Name Frame
            name_frame = tk.Frame(login_frame, bg=self.color["second_bg"])
            name_frame.place(x=0, y=0, width=(self.width - 251) / 2, height=300)

            name_label = tk.Label(name_frame, text="Name", bg=self.color["second_bg"],
                                  fg=self.fg, font=("Montserrat", 24, "bold"))
            name_label.pack(pady=15)
            name_input = tk.Entry(name_frame, width=23, bg=self.color["main_bg"], fg=self.fg)
            name_input.config(insertbackground=self.fg, font=("Montserrat", 23), justify=tk.CENTER)
            name_input.pack()

            # Password Frame
            password_frame = tk.Frame(login_frame, bg=self.color["second_bg"])
            password_frame.place(x=(self.width - 251) / 2, y=0, width=(self.width - 251) / 2, height=300)

            password_label = tk.Label(password_frame, text="Password", bg=self.color["second_bg"],
                                      fg=self.fg, font=("Montserrat", 24, "bold"))
            password_label.pack(pady=15)
            password_input = tk.Entry(password_frame, width=23, bg=self.color["main_bg"], fg=self.fg, show="*")
            password_input.config(insertbackground=self.fg, font=("Montserrat", 23), justify=tk.CENTER)
            password_input.pack()

            show_password = tk.Button(password_frame, text="Show", font=("Montserrat", 10))
            show_password.config(bg=self.color["main_bg"], fg=self.fg, activebackground=self.color["active_ground"],
                                 activeforeground=self.fg)
            show_password.bind("<Enter>", lambda x: show_password.config(bg=self.color["third_bg"]))
            show_password.bind("<Leave>", lambda x: show_password.config(bg=self.color["main_bg"]))
            show_password.bind("<Button-1>", lambda x: password_input.config(show=""))
            show_password.bind("<ButtonRelease-1>", lambda x: password_input.config(show="*"))
            show_password.pack(anchor=tk.NE, pady=10, padx=16)

            # Login Button
            login_button = tk.Button(login_frame, text="Login", font=("Montserrat", 26, "bold"), width=25)
            login_button.config(bg=self.color["main_bg"], fg=self.fg, activeforeground=self.fg,
                                activebackground=self.color["active_ground"], command=login_logic)
            login_button.bind("<Enter>", lambda x: login_button.config(bg=self.color["third_bg"]))
            login_button.bind("<Leave>", lambda x: login_button.config(bg=self.color["main_bg"]))
            login_button.pack(pady=225)

            # Useful Fast Binds
            name_input.focus_set()
            name_input.bind("<Return>", lambda x: password_input.focus_set())
            password_input.bind("<Return>", lambda x: login_button.invoke())

    def create_create_section(self):
        self.clear_login_content()

        user_options = {
            "Name",
            "Password",
            "Preferred Name",
        }
        # Label Frame
        basic_label_frame = tk.Frame(self.login_content_frame, bg=self.color["second_bg"])
        basic_label_frame.place(x=0, y=0, width=230, height=175)

        name_label = tk.Label(basic_label_frame, text="Name:")
        name_label.config(bg=self.color["second_bg"], fg=self.fg, font=("Montserrat", 20, "bold"))
        name_label.pack(anchor=tk.NE, pady=10)

        preferred_label = tk.Label(basic_label_frame, text="Preferred Name:")
        preferred_label.config(bg=self.color["second_bg"], fg=self.fg, font=("Montserrat", 20, "bold"))
        preferred_label.pack(anchor=tk.NE, pady=10)

        password_label = tk.Label(basic_label_frame, text="Password:")
        password_label.config(bg=self.color["second_bg"], fg=self.fg, font=("Montserrat", 20, "bold"))
        password_label.pack(anchor=tk.NE, pady=10)

        # Inputs for Labels
        basic_input_frame = tk.Frame(self.login_content_frame, bg=self.color["second_bg"])
        basic_input_frame.place(x=245, y=0, width=460, height=175)
        name_input = tk.Entry(basic_input_frame, fg=self.fg, insertbackground=self.fg, font=("Montserrat", 20),
                              bg=self.color["main_bg"])
        name_input.pack(fill=tk.X, pady=10)
        preferred_input = tk.Entry(basic_input_frame, fg=self.fg, insertbackground=self.fg, font=("Montserrat", 20),
                                   bg=self.color["main_bg"])
        preferred_input.pack(fill=tk.X, pady=12)
        password_input = tk.Entry(basic_input_frame, fg=self.fg, insertbackground=self.fg, font=("Montserrat", 20),
                                  bg=self.color["main_bg"], show="*")
        password_input.pack(fill=tk.X, pady=11)
        show_password_button = tk.Button(self.login_content_frame, text="Show")
        show_password_button.config(bg=self.color["main_bg"], fg=self.fg, font=("Montserrat", 15),
                                    activebackground=self.color["active_ground"], activeforeground=self.fg)
        show_password_button.place(x=720, y=127, width=60, height=37)
        show_password_button.bind("<Button-1>", lambda x: password_input.config(show=""))
        show_password_button.bind("<ButtonRelease-1>", lambda x: password_input.config(show="*"))
        show_password_button.bind("<Enter>", lambda x: show_password_button.config(bg=self.color["third_bg"]))
        show_password_button.bind("<Leave>", lambda x: show_password_button.config(bg=self.color["main_bg"]))

        # File options (Encryption, Name)
        file_options_frame = tk.Frame(self.login_content_frame, bg=self.color["second_bg"])
        file_options_frame.place(x=0, y=225, width=230, height=125)

        file_name_label = tk.Label(file_options_frame, text="Encrypt File:")
        file_name_label.config(bg=self.color["second_bg"], fg=self.fg, font=("Montserrat", 20, "bold"))
        file_name_label.pack(anchor=tk.NE, pady=10)

        file_name_label = tk.Label(file_options_frame, text="File Name:")
        file_name_label.config(bg=self.color["second_bg"], fg=self.fg, font=("Montserrat", 20, "bold"))
        file_name_label.pack(anchor=tk.NE, pady=10)

        # Input frame for the file options
        file_input_frame = tk.Frame(self.login_content_frame, bg=self.color["second_bg"])
        file_input_frame.place(x=245, y=225, width=460, height=125)

        encryption_options = ["No", "Yes"]
        encryption_selected = tk.StringVar()
        encryption_selected.set(encryption_options[0])
        encryption_dropdown = tk.OptionMenu(file_input_frame, encryption_selected, *encryption_options)
        encryption_dropdown.config(bg=self.color["main_bg"], font=("Montserrat", 14), fg=self.fg,
                                   activebackground=self.color["third_bg"], activeforeground=self.fg,
                                   highlightthickness=0)
        encryption_dropdown.pack(pady=10, anchor=tk.W)

        def fix_file_name():
            if " " in file_name_input.get():
                text = file_name_input.get().replace(' ', '-')
                file_name_input.delete(0, tk.END)
                file_name_input.insert(0, text)

        file_name_input = tk.Entry(file_input_frame, fg=self.fg, insertbackground=self.fg, font=("Montserrat", 20),
                                   bg=self.color["main_bg"])
        file_name_input.pack(fill=tk.X, pady=14)
        file_name_input.bind("<KeyRelease>", lambda x: fix_file_name())

        # Create Button
        def create_file():
            if name_input.get() == "" or name_input.get() is None:
                messagebox.showinfo("Create File Warning", "You need to put something into the Name box"
                                                           " to create a save file.")
                return
            elif preferred_input.get() == "" or preferred_input.get() is None:
                messagebox.showinfo("Create File Warning", "You need to put something into the Preferred "
                                                           "Name box to create a save file.")
                return
            elif password_input.get() == "" or password_input.get() is None:
                messagebox.showinfo("Create File Warning", "You need to put something into the Password "
                                                           "box to create a save file.")
                return
            elif file_name_input.get() == "" or file_name_input.get() is None:
                messagebox.showinfo("Create File Warning", "You need to put something into the File Name "
                                                           "box to create a save file.")
                return

            creator = self.controller.account_creator
            data = creator.create_base_account(name_input.get(), preferred_input.get(), password_input.get(),
                                               encryption_selected.get() == "Yes", js=True)
            creator.save_data(file_path=os.path.abspath("saves/" + file_name_input.get() + ".json"),
                              json_data=data, encrypted=encryption_selected.get() == "Yes")
            self.create_create_section()

        create_button = tk.Button(self.login_content_frame, text="Create Save File", command=lambda: create_file())
        create_button.config(bg=self.color["main_bg"], fg=self.fg, activeforeground=self.fg, width=40,
                             activebackground=self.color["active_ground"], font=("Montserrat", 20, "bold"))
        create_button.bind("<Enter>", lambda x: create_button.config(bg=self.color["third_bg"]))
        create_button.bind("<Leave>", lambda x: create_button.config(bg=self.color["main_bg"]))
        create_button.pack(side=tk.BOTTOM, pady=100)

    def proceed_without_account(self):
        self.clear_login_content()
        tk.Label(self.login_content_frame, text="Loading. . .", font=("Montserrat", 20, "bold"), fg=self.fg,
                 bg=self.color["second_bg"]).pack(expand=True)

        self.launcher.false_account = True

        user = self.launcher.account_controller.account_creator.create_base_account("Guest User", "Guest User",
                                                                                    "1234", False).copy()

        self.launcher.set_user_data(user.copy())
        self.exit()

    def create_options_content(self):
        login_with_account = tk.Button(self.login_options_frame, text="Login to Account",
                                       command=lambda: self.create_login_screen())
        login_with_account.config(bg=self.color["main_bg"], fg=self.fg, activeforeground=self.fg,
                                  activebackground=self.color["active_ground"], font=("Montserrat", 17, "bold"))
        login_with_account.bind("<Enter>", lambda x: login_with_account.config(bg=self.color["third_bg"]))
        login_with_account.bind("<Leave>", lambda x: login_with_account.config(bg=self.color["main_bg"]))
        login_with_account.pack(expand=True)

        create_account = tk.Button(self.login_options_frame, text="Create Account", width=14,
                                   command=lambda: self.create_create_section())
        create_account.config(bg=self.color["main_bg"], fg=self.fg, activeforeground=self.fg,
                              activebackground=self.color["active_ground"], font=("Montserrat", 17, "bold"))
        create_account.bind("<Enter>", lambda x: create_account.config(bg=self.color["third_bg"]))
        create_account.bind("<Leave>", lambda x: create_account.config(bg=self.color["main_bg"]))
        create_account.pack(expand=True)

        proceed_without = tk.Button(self.login_options_frame, text="Proceed Without", width=14,
                                    command=lambda: self.proceed_without_account())
        proceed_without.config(bg=self.color["main_bg"], fg=self.fg, activeforeground=self.fg,
                               activebackground=self.color["active_ground"], font=("Montserrat", 17, "bold"))
        proceed_without.bind("<Enter>", lambda x: proceed_without.config(bg=self.color["third_bg"]))
        proceed_without.bind("<Leave>", lambda x: proceed_without.config(bg=self.color["main_bg"]))
        proceed_without.pack(expand=True)

        self.root.bind("<Control-l>", lambda x: login_with_account.invoke())
        self.root.bind("<Control-c>", lambda x: create_account.invoke())
        self.root.bind("<Control-p>", lambda x: proceed_without.invoke())

    def create_frames(self):
        self.login_options_frame = tk.Frame(self.frame)
        self.login_options_frame.config(bg=self.color["second_bg"], highlightcolor=self.color["border_color"],
                                        highlightbackground=self.color["border_color"], highlightthickness=1)
        self.login_options_frame.place(x=0, y=self.height * 0.15, width=250, height=self.height * 0.85)

        self.login_content_frame = tk.Frame(self.frame)
        self.login_content_frame.config(bg=self.color["second_bg"], highlightcolor=self.color["border_color"],
                                        highlightbackground=self.color["border_color"], highlightthickness=1)
        self.login_content_frame.place(x=249, y=self.height * 0.15, width=self.width - 249, height=self.height * 0.85)

    def activate(self):
        self.launcher.reset_user_data()

        self.frame = tk.Frame(self.root)
        self.frame.config(bg=self.color["main_bg"])

        self.create_defaults_on_frame()
        self.create_frames()

        self.create_options_content()

        self.place()
