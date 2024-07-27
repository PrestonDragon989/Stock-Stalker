from window.layout.section import Section

from window.utils.website import OpenSite

from window.utils.popup import Popup
from tktooltip import ToolTip

import tkinter as tk

from matplotlib.figure import Figure as GraphFigure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import threading

from stocks.report import Report


class StockSearcherSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.bg = self.root_window.main_bg
        self.s_bg = self.root_window.second_bg
        self.t_bg = self.root_window.third_bg
        self.fg = self.root_window.fg

        self.search_frame = None
        self.display_frame = None

        self.sc = self.root_window.launcher.stock_client
        self.stock_data = None
        self.time_window = "max"
        self.stock_type = "Close"

        self.help = OpenSite()

        self.user_stock = self.root_window.launcher.user["stocks"] if (self.root_window.launcher.user is not
                                                                       None) else None

    def search_ticker(self, ticker) -> None:
        if ticker is None or ticker == "":
            return
        else:
            ticker = ticker.upper()
        waiting_text = tk.Label(self.display_frame, text="Loading. . .", font=("Montserrat", 20, "bold"))
        waiting_text.config(fg=self.fg, bg=self.s_bg)
        waiting_text.pack(anchor=tk.CENTER)
        self.stock_data = self.sc.get_data(ticker, self.time_window, ticker=True)
        if self.stock_data is False:
            waiting_text.destroy()
            Popup(self.root, self.root_window, true_root=True).activate(f"The ticker: {ticker} does not exist,"
                                                                        " or the connection timed out.", fontsize=18)
        else:
            self.display_frame.destroy()
            self.create_display_frame()
            if self.time_window == "1d":
                historical_data = self.stock_data.history(period=self.time_window, interval="90m")
            else:
                historical_data = self.stock_data.history(period=self.time_window)

            # Title of company
            title_frame = tk.Frame(self.display_frame, width=800, height=75)
            title_frame.config(bg=self.s_bg)

            name_title = tk.Label(title_frame, text=self.stock_data.info["longName"])
            name_title.config(fg=self.fg, bg=self.s_bg, font=("Montserrat", 25, "bold"))
            name_title.pack(pady=15)

            # Graph of stocks
            graph_frame = tk.Frame(self.display_frame, width=800, height=500)
            graph_frame.config(bg=self.t_bg)
            graph_frame.place(x=0, y=75, width=800, height=498)

            fig = GraphFigure(figsize=(8, 3), dpi=100)
            fig.patch.set_facecolor(self.s_bg)
            ax = fig.add_subplot(111)
            ax.patch.set_facecolor(self.bg)

            if self.stock_type == 'Volume':
                ax_label = 'Volume'
            elif self.stock_type == 'Dividends':
                ax_label = 'Dividends per Share Price'
            elif self.stock_type == 'Stock Splits':
                ax_label = 'Split Ratio'
            else:
                ax_label = f'{self.stock_type} Price'
            ax.plot(historical_data.index, historical_data[self.stock_type], label=ax_label,
                    color=self.root_window.sc)
            ax.set_title(f'{self.stock_data.info["longName"]}, {self.stock_type} Stocks', color=self.fg)
            ax.set_xlabel('Date', color=self.fg)
            if self.stock_type == 'Volume':
                y_label = 'Trading Volume'
            elif self.stock_type == 'Dividends':
                y_label = 'Dividends per Share (Dollars)'
            elif self.stock_type == 'Stock Splits':
                y_label = 'Split Ratio (New Shares per Old Share)'
            else:
                y_label = 'Price (Dollars)'
            ax.set_ylabel(y_label, color=self.fg)
            ax.tick_params(axis='both', colors=self.fg)
            ax.legend()
            ax.grid(color=self.root_window.gc)

            fig.subplots_adjust(left=0.075, right=0.98, top=0.95, bottom=0.1)

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

            # Sidebar
            sidebar_frame = tk.Frame(self.display_frame, width=100, height=575)
            sidebar_frame.config(bg=self.s_bg)
            sidebar_frame.place(x=791, y=3, height=570, width=100)

            tk.Frame(sidebar_frame, bg=self.t_bg).pack(pady=47)

            toolbar = NavigationToolbar2Tk(canvas, graph_frame, pack_toolbar=False)
            toolbar.config(bg="#f0f")
            toolbar.update()
            toolbar_buttons = {
                "Home": (toolbar.home, "Recenter Graph"),
                "Move": (toolbar.pan, "Move the graph around"),
                "Zoom": (toolbar.zoom, "Zoom in with RMB, and zoom out with LMB."),
                "Save": (toolbar.save_figure, "Export the current image of the graph to png.")
            }
            for button in toolbar_buttons:
                tool = tk.Button(sidebar_frame, text=button, command=toolbar_buttons[button][0], width=80)
                tool.config(bg=self.t_bg, fg=self.fg, activeforeground=self.fg, font=("Montserrat", 13),
                            activebackground=self.root_window.ag)
                tool.pack(pady=3)
                tool.bind("<Enter>", lambda event, b=tool: b.config(bg=self.bg))
                tool.bind("<Leave>", lambda event, b=tool: b.config(bg=self.t_bg))
                ToolTip(tool, msg=toolbar_buttons[button][1], delay=0.5)

            followed = self.user_stock["followed"]

            tk.Frame(sidebar_frame, bg=self.t_bg).pack(pady=10)

            def follow_logic(name):
                if ticker in followed:
                    followed.remove(ticker)
                    follow_button.config(text="Follow")
                else:
                    followed.append(ticker)
                    follow_button.config(text="Unfollow")
            follow_button = tk.Button(sidebar_frame, text="Follow" if ticker not in followed else "Unfollow",
                                      command=lambda: follow_logic(followed), width=80)
            follow_button.config(bg=self.t_bg, fg=self.fg, activeforeground=self.fg, font=("Montserrat", 13),
                                 activebackground=self.root_window.ag)
            follow_button.bind("<Enter>", lambda x: follow_button.config(bg=self.bg))
            follow_button.bind("<Leave>", lambda x: follow_button.config(bg=self.t_bg))
            ToolTip(follow_button, msg="Follow or Unfollow this ticker", delay=0.5)
            follow_button.pack(pady=3)

            def start_report():
                report = Report(self.root, self.root_window, self.root_window.launcher, ticker)
                report_thread = threading.Thread(target=report.activate, daemon=True)
                report_thread.start()
            report_button = tk.Button(sidebar_frame, text="Report", command=start_report, width=80)
            report_button.config(bg=self.t_bg, fg=self.fg, activeforeground=self.fg, font=("Montserrat", 13),
                                 activebackground=self.root_window.ag)
            report_button.bind("<Enter>", lambda x: report_button.config(bg=self.bg))
            report_button.bind("<Leave>", lambda x: report_button.config(bg=self.t_bg))
            ToolTip(report_button, msg=f"Get a report of the ticker {ticker}", delay=0.5)
            report_button.pack(pady=3)

            def set_new_type(*args):
                self.stock_type = selected_type.get()
                self.search_ticker(ticker)
            stock_types = ['Close', 'Open', 'Low', 'High', 'Volume', 'Dividends', 'Stock Splits']
            selected_type = tk.StringVar()
            selected_type.set(self.stock_type)
            selected_type.trace_add("write", set_new_type)
            dropdown_menu = tk.OptionMenu(sidebar_frame, selected_type, *stock_types)
            dropdown_menu.pack(pady=3)
            dropdown_menu.config(bg=self.t_bg, activebackground=self.bg, foreground=self.fg,
                                 activeforeground=self.fg, width=15, font=("Montserrat", 13))
            dropdown_menu.configure(highlightthickness=0)
            dropdown_menu["menu"].configure(bg=self.root_window.color["third_bg"], fg=self.fg)
            ToolTip(dropdown_menu, delay=0.5, msg="Change what you see about the ticker.")

            # Displaying Name Title
            title_frame.place(x=0, y=0, width=898, height=75)

    def create_search_frame(self) -> None:
        self.search_frame = tk.Frame(self.frame, height=125)
        self.search_frame.config(bg=self.s_bg, highlightcolor=self.root_window.border, highlightthickness=1,
                                 highlightbackground=self.root_window.border, height=75)
        self.search_frame.pack(fill=tk.X, expand=False)

        def to_uppercase():
            entry_text = ticker_input.get()
            ticker_input.delete(0, tk.END)
            ticker_input.insert(0, entry_text.upper())

        ticker_input = tk.Entry(self.search_frame, width=20)
        ticker_input.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 21),
                            justify='center', insertbackground=self.fg)
        ticker_input.pack(side=tk.LEFT, pady=8, padx=11)

        def threaded_search(ticker):
            search = threading.Thread(target=self.search_ticker, daemon=True, args=[ticker])
            search.start()

        search_button = tk.Button(self.search_frame, text="Search", width=10, activebackground=self.root_window.ag,
                                  activeforeground=self.fg,
                                  command=lambda: (to_uppercase(), threaded_search(ticker_input.get())))
        search_button.bind("<Enter>", lambda x: search_button.config(bg=self.bg))
        search_button.bind("<Leave>", lambda x: search_button.config(bg=self.t_bg))
        search_button.config(bg=self.t_bg, fg=self.fg, font=("Montserrat", 14))
        search_button.pack(side=tk.LEFT, pady=8, padx=5)
        try:
            self.root.bind("<Return>", lambda x: search_button.invoke())
        except:
            pass

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

        def set_new_window(*args):
            self.time_window = selected_time.get().lower()

        time_options = ['Max', 'YTD', '2Y', '1Y', '3Mo', '1Mo', '5D', '1D']
        selected_time = tk.StringVar()
        selected_time.set(time_options[0])
        selected_time.trace_add("write", set_new_window)
        dropdown_menu = tk.OptionMenu(self.search_frame, selected_time, *time_options)
        dropdown_menu.pack(side=tk.LEFT, pady=8, padx=5)
        dropdown_menu.config(bg=self.t_bg, activebackground=self.bg, foreground=self.fg,
                             activeforeground=self.fg, width=15, font=("Montserrat", 17))
        dropdown_menu.configure(highlightthickness=0)
        dropdown_menu["menu"].configure(bg=self.root_window.color["third_bg"], fg=self.fg)

    def create_display_frame(self) -> None:
        self.display_frame = tk.Frame(self.frame)
        self.display_frame.config(bg=self.s_bg, highlightcolor=self.root_window.border,
                                  highlightthickness=1, highlightbackground=self.root_window.border)
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
