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
        self._ticker = ticker
        self._mean_returns = None
        self._volatility = None

        self._annual_metrics_json = {}
        self._current_metrics_json = {}
        self._quotes_json = {}
        self._info_json = {}

        self.__get_metrics()
        self.__get_quotes()
        self.__get_company_info()
        self.__calculate_mean_returns_volatility()

    def show_api_key(self):
        print(self.client.api_key)

    def __get_company_info(self):
        self._info_json = self.client.company_profile(symbol=self._ticker)

    def __get_metrics(self):
        """Get financial metrics from Finnhub API
        :return: Financial Metrics for current year, and also list of annual KPI's for other years
        """
        metrics = self.client.company_basic_financials(self._ticker, "all")
        self._current_metrics_json = metrics.get("metric")
        if metrics.get("series"):
            self._annual_metrics_json = metrics["series"]["annual"]

    def __get_quotes(self):
        """Get quotes for stock for last 5 years.
        :return: quotes of stock with Open, High, Low, Close, Volume, Timestamp
        """
        _to, _from = create_unix_timestamps(365 * 5)  # 5 years
        self._quotes_json = self.client.stock_candles(self._ticker, "D", _from, _to)

    def get_quotes_df(self):
        """Transforms json quotes of stock into pandas DataFrame object.
        renaming columns, changing order, and transforming date timestamp to date
        :return:
        """
        data = pd.DataFrame(self._quotes_json)
        if data.empty:
            raise ValueError("The data frame with Quotes is empty!")
        data = rename_quotes_columns(data)
        data["Date"] = pd.to_datetime(data["Date"], unit="s").dt.date
        return data[["Date", "Open", "Low", "High", "Close", "Volume"]].set_index("Date")

    def get_current_metrics_df(self):
        current = pd.DataFrame(self._current_metrics_json.items())
        current.columns = ["KPI", "Value"]
        return current

    # Todo define which kpi can be useful to calculate some metrics for portfolio.

    def _transform_annual_metrics_to_data_frame(self):
        return pd.DataFrame.from_dict(self._annual_metrics_json, orient='index').transpose()

    def __calculate_mean_returns_volatility(self):
        returns = calculate_daily_returns(self.get_quotes_df()["Close"])
        self._mean_returns = calculate_mean_daily_returns(returns)
        self._volatility = calculate_std_of_returns(returns)