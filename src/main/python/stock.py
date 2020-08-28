from utils import *
import finnhub as fh
import os
import pandas as pd
from returns import *


api_key = os.environ.get("FH_API_KEY")

if not api_key:
    raise KeyError(
        "There is no API KEY for Finnhub\nPlease visit https://finnhub.io/docs/api to get your free api key"
    )


class Stock:

    client = fh.Client(api_key)

    def __init__(self, ticker):
        self.ticker = ticker
        self.mean_returns = None
        self.volatility = None
        self.log_daily_returns: pd.DataFrame

        self.__annual_metrics_json = {}
        self.__current_metrics_json = {}
        self.__quotes_json = {}
        self.__info_json = {}

        self.__get_metrics()
        self.__get_quotes()
        self.__get_company_info()
        self.__calculate_returns_and_volatility()

    # Public methods

    def get_quotes_df(self):
        """Transforms json quotes of stock into pandas DataFrame object.
        renaming columns, changing order, and transforming date timestamp to date
        :return:
        """
        data = pd.DataFrame(self.__quotes_json)
        if data.empty:
            raise ValueError("The data frame with Quotes is empty!")
        data = rename_quotes_columns(data)
        data["Date"] = pd.to_datetime(data["Date"], unit="s").dt.date
        return data[["Date", "Close"]].set_index("Date")

    def get_current_metrics_df(self):
        current = pd.DataFrame(self.__current_metrics_json.items())
        current.columns = ["KPI", "Value"]
        return current

    # Private methods

    def __get_company_info(self):
        """Get basic company information
        :return: json with company information
        """
        self.__info_json = self.client.company_profile(symbol=self.ticker)

    def __get_metrics(self):
        """Get financial metrics from Finnhub API
        :return: Financial Metrics for current year, and also list of annual KPI's for other years
        """
        metrics = self.client.company_basic_financials(self.ticker, "all")
        self.__current_metrics_json = metrics.get("metric")

        if metrics.get("series"):
            self.__annual_metrics_json = metrics["series"]["annual"]

    def __get_quotes(self):
        """Get quotes for stock for last 5 years.
        :return: quotes of stock with Open, High, Low, Close, Volume, Timestamp
        """
        _to, _from = create_unix_timestamps(365 * 5)  # 5 years
        self.__quotes_json = self.client.stock_candles(self.ticker, "D", _from, _to)

    def __calculate_returns_and_volatility(self):
        """Calculates mean return, volatility and daily log returns
        :return: log daily returns, mean returns, volatility
        """
        close_prices = self.get_quotes_df()
        self.log_daily_returns = calculate_daily_logarithmic_returns(close_prices)
        self.mean_returns = self.log_daily_returns.values.mean()
        self.volatility = self.log_daily_returns.values.std()
