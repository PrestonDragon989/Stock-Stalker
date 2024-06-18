from window.layout.section import Section

from window.utils.website import OpenSite

import tkinter as tk


class StockSearcherSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.bg = self.root_window.main_bg
        self.s_bg = self.root_window.second_bg
        self.t_bg = self.root_window.third_bg
        self.fg = self.root_window.fg

        self.search_frame = None
        self.display_frame = None

        self.help = OpenSite()

    def search_ticker(self, ticker) -> None:
        print(f"Searching ticker: " + str(ticker))
        for x in self.search_frame.winfo_children():
            print(x)

    def create_search_frame(self) -> None:
        self.search_frame = tk.Frame(self.frame, height=125)
        self.search_frame.config(bg=self.s_bg, highlightcolor="black", highlightthickness=1,
                                 highlightbackground="black", height=75)
        self.search_frame.pack(fill=tk.X, expand=False)

        ticker_input = tk.Entry(self.search_frame, width=20)
        ticker_input.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 21),
                            justify='center', insertbackground=self.fg)
        ticker_input.pack(side=tk.LEFT, pady=8, padx=11)

        search_button = tk.Button(self.search_frame, text="Search", width=10, activebackground=self.root_window.ag,
                                  activeforeground=self.fg, command=lambda: self.search_ticker(ticker_input.get()))
        search_button.bind("<Enter>", lambda x: search_button.config(bg=self.bg))
        search_button.bind("<Leave>", lambda x: search_button.config(bg=self.t_bg))
        search_button.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 14))
        search_button.pack(side=tk.LEFT, pady=8, padx=5)
        self.root.bind("<Return>", lambda x: search_button.invoke())

        help_button = tk.Button(self.search_frame, text="Help", width=10, activebackground=self.root_window.ag,
                                activeforeground=self.fg, command=self.help.open_docs)
        help_button.bind("<Enter>", lambda x: help_button.config(bg=self.bg))
        help_button.bind("<Leave>", lambda x: help_button.config(bg=self.t_bg))
        help_button.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 14))
        help_button.pack(side=tk.RIGHT, pady=8, padx=5)

        ticker_button = tk.Button(self.search_frame, text="Search Tickers", width=15,
                                  activebackground=self.root_window.ag, activeforeground=self.fg,
                                  command=self.help.open_yahoo)
        ticker_button.bind("<Enter>", lambda x: ticker_button.config(bg=self.bg))
        ticker_button.bind("<Leave>", lambda x: ticker_button.config(bg=self.t_bg))
        ticker_button.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 14))
        ticker_button.pack(side=tk.RIGHT, pady=8, padx=5)

    def create_display_frame(self) -> None:
        self.display_frame = tk.Frame(self.frame)
        self.display_frame.config(bg=self.s_bg, highlightcolor="black",
                                  highlightthickness=1, highlightbackground="black")
        self.display_frame.pack(fill=tk.BOTH, expand=True)

    def activate(self):
        title = tk.Label(self.frame, text="Stock Searcher", font=("Montserrat", 32, "bold"))
        title.config(bg=self.bg, fg=self.fg)
        title.pack(pady=5)

        self.create_search_frame()
        self.create_display_frame()

        super().place()

    def hide(self):
        super().hide()
        self.root.unbind("<Return>")

