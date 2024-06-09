from window.layout.section import Section

import tkinter as tk


class StockSearcherSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

    def activate(self):
        title = tk.Label(self.frame, text="Stock Searcher", font=("Montserrat", 32, "bold"))
        title.config(bg=self.bg, fg=self.fg)
        title.pack(pady=5)

        super().place()

