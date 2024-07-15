import tkinter as tk


class Popup:
    def __init__(self, root, root_window, true_root=False):
        self.root = root
        self.root_window = root_window

        self.true_root = true_root

    def activate(self, text, fontsize=15):
        if not self.true_root:
            popup = tk.Toplevel(self.root)
        else:
            popup = tk.Tk()
            popup.bind("<<RootDestroy>>", lambda x: popup.destroy())
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

        popup.bind("<Return>", lambda x: close.invoke())
        popup.focus()

        popup.mainloop()
