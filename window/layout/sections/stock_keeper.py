from stocks.report import Report
from window.layout.section import Section

import tkinter as tk
from tkinter import ttk
from tktooltip import ToolTip

from matplotlib.figure import Figure as GraphFigure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import threading

from window.utils.website import OpenSite


class StockKeeperSection(Section):
    def __init__(self, root, root_window):
        super().__init__(root, root_window, root_window.main_bg, root_window.fg)

        self.site = OpenSite()

        self.color = self.root_window.color

        self.scroll_bar = None
        self.keeper_container = None
        self.keeper_frame = None

        self.control_bar = None
        self.stock_type = "Close"
        self.time_window = "max"

        self.results_frame = None
        self.tickers_done = []

        self.scroll_style = ttk.Style()
        self.scroll_style.theme_use('classic')
        self.scroll_style.configure("Vertical.TScrollbar",
                                    gripcount=0,
                                    lightcolor=self.bg,
                                    darkcolor=self.bg,
                                    background=self.color["third_bg"],
                                    troughcolor=self.color["second_bg"],
                                    bordercolor=self.color["border_color"],
                                    arrowcolor=self.color["third_bg"])
        self.scroll_style.map("Vertical.TScrollbar",
                              background=[("active", self.color["third_bg"])])

        self.sc = self.root_window.launcher.stock_client
        self.user_stock = self.root_window.launcher.user["stocks"] if (self.root_window.launcher.user is not
                                                                       None) else None
        self.user = self.root_window.launcher.user

    def set_containers(self):
        # Setting Up initial scrolling & frames
        self.keeper_container = tk.Canvas(self.frame, bg=self.bg, highlightthickness=1, highlightcolor=self.bg,
                                          highlightbackground=self.bg)
        self.scroll_bar = ttk.Scrollbar(self.keeper_container, orient="vertical",
                                        command=self.keeper_container.yview, style="Vertical.TScrollbar")

        self.keeper_frame = tk.Frame(self.keeper_container, bg=self.color["border_color"])
        self.keeper_frame.bind("<Configure>", lambda e: self.keeper_container.configure(
            scrollregion=self.keeper_container.bbox("all")))

        self.keeper_container.configure(yscrollcommand=self.scroll_bar.set)
        self.keeper_container.create_window((0, 0), window=self.keeper_frame, anchor="nw", width=880)
        self.keeper_container.pack(side="left", fill="both", expand=True)
        self.scroll_bar.pack(side="right", fill="y")

    def bind_widgets_to_scroll(self, widget, canvas):
        widget.bind("<MouseWheel>", lambda e: canvas.yview_scroll(
            int(-1 * (e.delta / 120)), "units"))
        for child in widget.winfo_children():
            self.bind_widgets_to_scroll(child, canvas)

    def reset(self):
        for widget in self.keeper_frame.winfo_children():
            threading.Thread(target=widget.destroy, daemon=True).start()

        def continue_reset():
            self.tickers_done = []
            self.setup_content()
            self.bind_widgets_to_scroll(self.frame, self.keeper_container)
        threading.Thread(target=continue_reset, daemon=True).start()

    def setup_control_bar(self):
        reset_button = tk.Button(self.control_bar, text="Reset Tickers", command=lambda: self.reset(), width=16)
        reset_button.config(bg=self.color["third_bg"], fg=self.fg, font=("Montserrat", 14),
                            activebackground=self.color["active_ground"], activeforeground=self.fg)
        reset_button.bind("<Enter>", lambda x: reset_button.config(bg=self.bg))
        reset_button.bind("<Leave>", lambda x: reset_button.config(bg=self.color["third_bg"]))
        reset_button.pack(side=tk.LEFT, pady=8, padx=5)

        help_button = tk.Button(self.control_bar, text="Keeper Help", command=lambda: self.site.open_docs(), width=16)
        help_button.config(bg=self.color["third_bg"], fg=self.fg, font=("Montserrat", 14),
                           activebackground=self.color["active_ground"], activeforeground=self.fg)
        help_button.bind("<Enter>", lambda x: help_button.config(bg=self.bg))
        help_button.bind("<Leave>", lambda x: help_button.config(bg=self.color["third_bg"]))
        help_button.pack(side=tk.LEFT, pady=8, padx=5)

        def set_new_window(*args):
            self.time_window = selected_time.get().lower()
            self.reset()
        time_options = ['Max', 'YTD', '2Y', '1Y', '3Mo', '1Mo', '5D', '1D']
        selected_time = tk.StringVar()
        selected_time.set(self.time_window)
        selected_time.trace_add("write", set_new_window)
        dropdown_menu = tk.OptionMenu(self.control_bar, selected_time, *time_options)
        dropdown_menu.pack(side=tk.RIGHT, pady=8, padx=5)
        dropdown_menu.config(bg=self.color["third_bg"], activebackground=self.bg, foreground=self.fg,
                             activeforeground=self.fg, width=14, font=("Montserrat", 17))
        dropdown_menu.configure(highlightthickness=0)
        dropdown_menu["menu"].configure(bg=self.color["third_bg"], fg=self.fg)

        def set_new_type(*args):
            self.stock_type = selected_type.get().lower()
            self.reset()
        type_options = ['Close', 'Open', 'Low', 'High', 'Volume', 'Dividends', 'Stock Splits']
        selected_type = tk.StringVar()
        selected_type.set(self.stock_type)
        selected_type.trace_add("write", set_new_type)
        dropdown = tk.OptionMenu(self.control_bar, selected_type, *type_options)
        dropdown.pack(side=tk.RIGHT, pady=8, padx=5)
        dropdown.config(bg=self.color["third_bg"], activebackground=self.bg, foreground=self.fg,
                        activeforeground=self.fg, width=14, font=("Montserrat", 17))
        dropdown.configure(highlightthickness=0)
        dropdown["menu"].configure(bg=self.color["third_bg"], fg=self.fg)

    def setup_content(self):
        # Setting Up Results & Bar
        self.control_bar = tk.Frame(self.keeper_frame)
        self.control_bar.config(bg=self.color["second_bg"], highlightcolor=self.color["border_color"],
                                highlightbackground=self.color["border_color"], highlightthickness=1)
        self.control_bar.pack(fill=tk.X, expand=True)

        self.setup_control_bar()

        tickers = self.user_stock["followed"]
        stock_data = self.sc.get_tickers(" ".join(tickers), session=self.sc.keeper_session)
        for i, followed in enumerate(tickers):
            if followed in self.tickers_done:
                continue
            else:
                self.tickers_done.append(followed)

            def show_followed(follow):
                ticker = stock_data.tickers[follow]
                if self.time_window == "1d":
                    historical_data = ticker.history(period=self.time_window, interval="90m")
                else:
                    historical_data = ticker.history(period=self.time_window)
                try:
                    base_frame = tk.Frame(self.keeper_frame, bg=self.color["second_bg"])
                    base_frame.pack(fill=tk.X, expand=True, pady=1)
                except tk.TclError:
                    print("tk.TclError Occured :) Not My Problem <3")
                    return

                title_frame = tk.Frame(base_frame, bg=self.color["second_bg"], width=799, height=80)
                title_frame.pack()
                title = tk.Label(title_frame, text=ticker.info["longName"])
                title.config(fg=self.fg, bg=self.color["second_bg"], font=("Montserrat", 25, "bold"))
                title.pack(anchor=tk.CENTER)

                def show_data():
                    data_frame = tk.Frame(base_frame, bg=self.color["second_bg"])
                    data_frame.pack(fill=tk.X, expand=True)

                    graph_frame = tk.Frame(data_frame, width=199, height=600, bg="#f0f")
                    graph_frame.pack(side=tk.LEFT, anchor=tk.W)

                    fig = GraphFigure(figsize=(8, 3), dpi=100)
                    fig.patch.set_facecolor(self.color["second_bg"])
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
                    ax.set_title(f'{ticker.info["longName"]}, {self.stock_type} Stocks', color=self.fg)
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

                    fig.subplots_adjust(left=0.075, right=0.96, top=0.88, bottom=0.1)

                    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
                    canvas.draw()
                    canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

                    # Buttons
                    sidebar_frame = tk.Frame(base_frame, width=130, height=575)
                    sidebar_frame.config(bg=self.color["second_bg"])
                    sidebar_frame.place(x=775, y=60, width=100, height=575)

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
                        tool.config(bg=self.color["third_bg"], fg=self.fg,
                                    activeforeground=self.fg, font=("Montserrat", 13),
                                    activebackground=self.root_window.ag)
                        tool.pack(pady=3)
                        tool.bind("<Enter>", lambda event, b=tool: b.config(bg=self.bg))
                        tool.bind("<Leave>", lambda event, b=tool: b.config(bg=self.color["third_bg"]))
                        ToolTip(tool, msg=toolbar_buttons[button][1], delay=0.5)

                    tk.Frame(sidebar_frame, bg=self.color["third_bg"]).pack(pady=10)

                    def follow_logic(followed_tickers):
                        if follow in self.user["stocks"]["followed"]:
                            followed_tickers.remove(follow)
                            follow_button.config(text="Follow")
                        else:
                            followed_tickers.append(follow)
                            follow_button.config(text="Unfollow")
                        self.user["stocks"]["followed"] = followed_tickers
                        self.reset()

                    follow_button = tk.Button(sidebar_frame,
                                              text="Follow" if follow not in self.user_stock["followed"]
                                              else "Unfollow",
                                              command=lambda: follow_logic(self.user_stock["followed"]), width=80)
                    follow_button.config(bg=self.color["third_bg"], fg=self.fg, activeforeground=self.fg,
                                         font=("Montserrat", 13),
                                         activebackground=self.root_window.ag)
                    follow_button.bind("<Enter>", lambda x: follow_button.config(bg=self.bg))
                    follow_button.bind("<Leave>", lambda x: follow_button.config(bg=self.color["third_bg"]))
                    ToolTip(follow_button, msg="Unfollow this ticker", delay=0.5)
                    follow_button.pack(pady=3)

                    def start_report():
                        report = Report(self.root, self.root_window, self.root_window.launcher, follow)
                        report_thread = threading.Thread(target=report.activate, daemon=True)
                        report_thread.start()

                    report_button = tk.Button(sidebar_frame, text="Report", command=start_report, width=80)
                    report_button.config(bg=self.color["third_bg"], fg=self.fg,
                                         activeforeground=self.fg, font=("Montserrat", 13),
                                         activebackground=self.root_window.ag)
                    report_button.bind("<Enter>", lambda x: report_button.config(bg=self.bg))
                    report_button.bind("<Leave>", lambda x: report_button.config(bg=self.color["third_bg"]))
                    ToolTip(report_button, msg=f"Get a report of the ticker {follow}", delay=0.5)
                    report_button.pack(pady=3)

                    self.bind_widgets_to_scroll(base_frame, self.keeper_container)

                show_data()

            show_followed(followed)

    def activate(self):
        for widget in self.frame.winfo_children():
            threading.Thread(target=widget.destroy, daemon=True)

        self.set_containers()

        def continue_activate():
            self.tickers_done = []
            self.setup_content()

            self.bind_widgets_to_scroll(self.frame, self.keeper_container)
        threading.Thread(target=continue_activate, daemon=True).start()

        super().place()
