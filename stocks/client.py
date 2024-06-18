import yfinance as yf
import pandas as pd

from tkinter import messagebox


def ticker_exists(ticker_symbol, time="1d") -> False or (True, pd.DataFrame):
    """
    Tries to find the given ticker. It will wait for it to time out, or an error to pass false. Otherwise, returns true.
    Args:
        ticker_symbol: The Ticker of the stock you are trying to get.
        time: Only relevant if you want the data back. This defines how far back to search.

    Returns:
        Returns True if ticker found, or false if not found.
    """
    try:
        # Attempt to fetch the ticker's information
        stock_data = yf.Ticker(ticker_symbol)
        historical_data = stock_data.history(period=time)
        if historical_data.empty:
            return False
        return True, historical_data
    except Exception as e:
        print("TICKER EXTRACTION FAILED:", e)
        return False


def get_data(ticker_symbol, time) -> False or pd.DataFrame:
    """
    Gets the ticker data if it exists, & returns it. If not, returns False.
    Args:
        ticker_symbol: This is the ticker that is searched.
        time: This controls the range of time we use. Options are: 1d, 5d, 1mo, 3mo, 1y, 2y, ytd, max

    Returns:
        Either false if the ticker couldn't be gotten, but if it could, a DataFrame of the stocks.
    """
    ticker_data = ticker_exists(ticker_symbol, time=time)
    if ticker_data is False:
        messagebox.showerror("STALKER Error", f"The ticker: {ticker_symbol.upper()}" 
                                              "doesn't exist, or the request to find it timed out." 
                                              "Check your internet & permissions.")
        return False
    return ticker_data


print(get_data("GME", "5d"))
