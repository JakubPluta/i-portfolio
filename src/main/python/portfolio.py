from stock import Stock
from weights_optimizer import WeightsOptimizer


class Portfolio:

    ASSETS = 0

    def __init__(self):
        self.__tickers = []
        self.__weights = []
        self._portfolio = {}

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

    def set_weights(self, tickers: dict):
        """
        :param tickers: dictionary with ticker list
        :return:
        """
        self.__weights = tickers.values

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
                self.ASSETS += 1
                self.__tickers.append(Stock(ticker))
                self.__weights.append(weight)
            self.__calculate_weights()
        self.__zip_portfolio()

    def __calculate_weights(self):
        # It needs to be always equal to 1
        self.__weights = [1/len(self.__tickers) for ticker in self.__tickers]

    def __validate_weights(self):
        if not sum(self.__weights) == 1:
            raise ValueError("Weights of all assets needs to be equal to 1\n"
                             "All of weights was set-up into equal.\n"
                             "If you want to change weights use set_weights() method")
        self.__weights = [1 / len(self.__tickers) for ticker in self.__tickers]

    def __zip_portfolio(self):
        if self.__weights and self.__tickers and len(self.__weights) == len(self.__tickers):
            self._portfolio = dict(zip(self.__tickers, self.__weights))

    @staticmethod
    def _validate_ticker(ticker: Stock):
        if not ticker._info:
            raise TypeError(f"Nothing found for given ticker {ticker}")
        elif not isinstance(ticker, Stock):
            raise TypeError("Provided ticker is not instance of Stock")
