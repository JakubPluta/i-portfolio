from utils import *
import finnhub as fh
import os
import pandas as pd

api_key = os.environ.get("FH_API_KEY")


class Stock:

    client = fh.Client(api_key)

    def __init__(self, ticker):
        self._ticker = ticker
        self._annual_metrics = {}
        self._current_metrics = {}
        self._quotes = {}
        self._info = {}

        self.get_metrics()
        self.get_quotes()
        self.__get_company_info()

    def __get_company_info(self):
        self._info = self.client.company_profile(symbol=self._ticker)

    def get_metrics(self):
        """Get financial metrics from Finnhub API
        :return: Financial Metrics for current year, and also list of annual KPI's for other years
        """

        metrics = self.client.company_basic_financials(self._ticker, "all")

        self._current_metrics = metrics.get("metric")

        if metrics.get("series"):
            self._annual_metrics = metrics['series']["annual"]

    def get_quotes(self):
        """Get quotes for stock for last 5 years.
        :return: quotes of stock with Open, High, Low, Close, Volume, Timestamp
        """
        _to, _from = create_unix_timestamps(365*5)  # 5 years
        quotes = self.client.stock_candles(self._ticker, "D", _from, _to)
        self._quotes = quotes



a = Stock("AMZN")

print(a)