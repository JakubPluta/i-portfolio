from client import Stock


class Portfolio:
    PORTFOLIO_ITEMS = 0

    def __init__(self):
        self.__tickers = []
        self.__weights = {}

    @staticmethod
    def _validate_ticker(ticker: Stock):
        if not ticker._info:
            raise TypeError(f"Nothing found for given ticker {ticker}")
        elif not isinstance(ticker, yf.Ticker):
            raise TypeError("Provided ticker is not instance of yfinance Ticker")

    def add_stock_to_portfolio(self, ticker):
        if isinstance(ticker, str):
            ticker = Stock(ticker)
            self.__tickers.append(ticker)
            self.PORTFOLIO_ITEMS += 1
        elif isinstance(ticker,list):
            for tick in ticker:
                tick = Stock(tick)
                self.__tickers.append(tick)
                self.PORTFOLIO_ITEMS += 1
        else:
            raise ValueError("Please enter single ticker, or list of tickers")

    def delete_stock_from_portfolio(self, ticker):
        try:
            self.__tickers.remove(ticker)
        except KeyError:
            print("Ticker not found")

    def show_portfolio_items(self):
        for i in self.__tickers:
            print(i)
