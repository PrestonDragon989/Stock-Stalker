import tkinter as tk

import pandas as pd


class StockGraph:
    def __init__(self, root, root_window, dataframe):
        self.root = root
        self.root_window = root_window

        self.dataframe = dataframe
    