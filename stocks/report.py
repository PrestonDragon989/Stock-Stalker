import tkinter as tk


class Report:
    def __init__(self, root, root_window, launcher, ticker):
        self.root = root
        self.root_window = root_window

        self.launcher = launcher
        self.client = self.launcher.stock_client

        self.ticker = ticker
        self.ticker_data = None
        self.quick_ticker_info = {}

        self.color = self.root_window.color

        self.window = None
        self.size = (800, 600)

    def run_ticker_query(self):
        self.ticker_data = self.client.get_data(self.ticker, "1d", ticker=True)
        self.quick_ticker_info["name"] = self.ticker_data.info["longName"]

        for thing in self.ticker_data.info:
            print(thing, ": ", self.ticker_data.info[thing])
        hist = self.ticker_data.history("1d")
        print(hist.columns)

    def window_config(self):
        self.window.title(f"{self.quick_ticker_info["name"]} Report")
        self.window.resizable(False, False)
        self.window.geometry(f"{self.size[0]}x{self.size[1]}")
        self.window.config(bg=self.color["main_bg"])

    def activate(self):
        self.run_ticker_query()

        self.window = tk.Tk()
        self.window_config()

        self.window.mainloop()
