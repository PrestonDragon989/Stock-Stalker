from tktooltip import ToolTip

from window.layout.section import Section

import tkinter as tk

from window.utils.website import OpenSite


class DataSrcSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.paragraph_text = f"""The data collected on all of the stocks seen is from Yahoo! Finance.
What this means, is that any data gotten is reliant on them, and inaccuracies can occur at their hand. 
This makes it somewhat unreliable, however it also free, hence the choice.
Any mistakes made at the hand of false data cannot be blamed on the creator of {self.root_window.launcher.name}. 


All collections are ran through them, and any data about the stalks or crypto currencies can be found through them.
This is simply a tool to help you manage any stocks, as well as make decisions. 




To visit the site, press the button below."""

        self.site = OpenSite()

    def activate(self):
        def visit_site():
            self.site.open_yahoo()

        title = tk.Label(self.frame, text="Stock Data Source", font=("Montserrat", 32, "bold"))
        title.config(bg=self.bg, fg=self.fg)
        title.pack(pady=6)

        explanation = tk.Label(self.frame, text=self.paragraph_text,
                               font=("Montserrat", 15),
                               wraplength=(self.root_window.size[0] - self.root_window.taskbar.width) * 0.75,
                               bg=self.bg, fg=self.fg)
        explanation.pack(pady=15)

        yfinance_page = tk.Button(self.frame, text="Visit Site", font=("Montserrat", 32, "bold"), command=visit_site,
                                  width=20)
        yfinance_page.config(width=20, bg=self.root_window.second_bg, fg=self.root_window.fg,
                             font=("Montserrat", 32, "bold"), activebackground=self.root_window.ag,
                             activeforeground=self.root_window.fg, highlightcolor=self.root_window.third_bg)
        yfinance_page.bind("<Enter>", lambda event: yfinance_page.config(bg=self.root_window.third_bg))
        yfinance_page.bind("<Leave>", lambda event: yfinance_page.config(bg=self.root_window.second_bg))
        yfinance_page.pack(pady=25)
        ToolTip(yfinance_page, msg=f"Visit site {self.site.yahoo_site}", delay=0.5)

        super().place()
