import tkinter as tk


class Popup:
    def __init__(self, root, root_window):
        self.root = root
        self.root_window = root_window

    def activate(self, text, fontsize=15):
        popup = tk.Toplevel(self.root)
        popup.title(f"{self.root_window.launcher.name} Alert")
        popup.resizable(False, False)
        popup.geometry("300x200")
        popup.config(bg=self.root_window.main_bg)

        text = tk.Label(popup, text=text, wraplength=300)
        text.config(bg=self.root_window.main_bg, fg=self.root_window.fg, font=("Montserrat", fontsize))
        text.pack(pady=2)

        close = tk.Button(popup, text="Close", command=popup.destroy)
        close.config(bg=self.root_window.second_bg, fg=self.root_window.fg,
                     font=("Montserrat", 17, "bold"), activebackground=self.root_window.ag,
                     activeforeground=self.root_window.fg, highlightcolor=self.root_window.third_bg)
        close.pack(side=tk.BOTTOM, pady=10)
        close.bind("<Enter>", lambda x: close.config(bg=self.root_window.third_bg))
        close.bind("<Leave>", lambda x: close.config(bg=self.root_window.second_bg))

        popup.mainloop()
