import yfinance as yf
import pandas as pd

from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    """ Special Session class that optimizes the requests, caches data, adds limiters. This makes it so Yahoo doesn't
    have a spasm about a ton of requests, and doesn't start fighting back. """
    pass


""" The session question. This is contains the limit (2 requests per 5 seconds), the memory bucket, and the cache. This
is the session that is fed into the requests. """
basic_session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)

keeper_session = CachedLimiterSession(
    limiter=Limiter(RequestRate(3, Duration.SECOND*4)),  # max 3 requests per 4 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)


def ticker_exists(ticker_symbol, session=basic_session) -> False or (True, yf.Tickers):
    """
    Tries to find the given ticker. It will wait for it to time out, or an error to pass false. Otherwise, returns true.
    Args:
        ticker_symbol: The Ticker of the stock you are trying to get.
        session: this is for custom sessions

    Returns:
        Returns True if ticker found, or false if not found.
    """
    try:
        # Attempt to fetch the ticker's information
        stock_data = yf.Ticker(ticker_symbol, session=session)
        historical_data = stock_data.history(period="1d")
        if historical_data.empty:
            return False
        return True, stock_data
    except Exception as e:
        print("TICKER EXTRACTION FAILED:", e)
        return False


def get_data(ticker_symbol, time, ticker=False, session=basic_session) -> False or pd.DataFrame or yf.Ticker:
    """
    Gets the ticker data if it exists, & returns it. If not, returns False.
    Args:
        ticker_symbol: This is the ticker that is searched.
        time: This controls the range of time we use. Options are: 1d, 5d, 1mo, 3mo, 1y, 2y, ytd, max
        ticker: If this is true, it returns the whole ticker & not just the history. If this is true, time isn't needed.
        session: For specific session

    Returns:
        Either false if the ticker couldn't be gotten, but if it could, a DataFrame of the stocks / yf Ticker.
    """
    ticker_data = ticker_exists(ticker_symbol, session=session)
    if type(ticker_data) is not tuple:
        return False
    elif ticker:
        return ticker_data[1]
    else:
        return ticker_data.history(period=time)


def get_tickers(tickers, session=basic_session) -> yf.Tickers:
    """
    This just returns a Tickers class that contains all the ticker data given. To access the data, do data["ticker"],
    and then you have access to that. It uses the current session.
    Args:
        tickers: This is a string of the tickers. Example: "aapl f gme"
        session: For specific sessions

    Returns:
        yf.Tickers
    """
    return yf.Tickers(tickers, session=session)
