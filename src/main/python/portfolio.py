from stock import Stock


class Portfolio:

    ASSETS = 0

    def __init__(self):
        self.__tickers = []
        self.__weights = []

    @staticmethod
    def _validate_ticker(ticker: Stock):
        if not ticker._info:
            raise TypeError(f"Nothing found for given ticker {ticker}")
        elif not isinstance(ticker, Stock):
            raise TypeError("Provided ticker is not instance of Stock")

    def add_stock_to_portfolio(self, ticker):
        if isinstance(ticker, str):
            ticker = Stock(ticker)
            self.__tickers.append(ticker)
            self.ASSETS += 1
        elif isinstance(ticker, list):
            for tick in ticker:
                tick = Stock(tick)
                self.__tickers.append(tick)
                self.ASSETS += 1
        else:
            raise ValueError("Please enter single ticker, or list of tickers")

    def delete_stock_from_portfolio(self, ticker):
        try:
            self.__tickers.remove(ticker)
        except KeyError:
            print("Ticker not found")

    def show_portfolio_items(self):
        for ticker in self.__tickers:
            print(ticker)

    def create_portfolio(self, tickers: (dict, list)):
        if isinstance(tickers, list):
            for ticker in tickers:
                self.__tickers.append(Stock(ticker))
                self.ASSETS += 1
            self.__calculate_weights()

        elif isinstance(tickers, dict):
            for ticker, weight in tickers.items():
                self.__tickers.append(Stock(ticker))
                self.__weights.append(weight)

    def __calculate_weights(self):
        # It needs to be always equal to 1
        self.__weights = [1/len(self.__tickers) for ticker in self.__tickers]
