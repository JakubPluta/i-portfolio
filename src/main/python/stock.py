from utils import *
import finnhub as fh
import os
import pandas as pd

api_key = os.environ.get("FH_API_KEY")

if not api_key:
    raise KeyError(
        "There is no API KEY for Finnhub\nPlease visit https://finnhub.io/docs/api to get your free api key"
    )


class Stock:

    client = fh.Client(api_key)

    def __init__(self, ticker):
        self._ticker = ticker
        self._annual_metrics_json = {}
        self._current_metrics_json = {}
        self._quotes_json = {}
        self._info_json = {}

        self.get_metrics()
        self.get_quotes()
        self.get_company_info()

    def show_api_key(self):
        print(self.client.api_key)

    def get_company_info(self):
        self._info_json = self.client.company_profile(symbol=self._ticker)

    def get_metrics(self):
        """Get financial metrics from Finnhub API
        :return: Financial Metrics for current year, and also list of annual KPI's for other years
        """
        metrics = self.client.company_basic_financials(self._ticker, "all")
        self._current_metrics_json = metrics.get("metric")
        if metrics.get("series"):
            self._annual_metrics_json = metrics["series"]["annual"]

    def get_quotes(self):
        """Get quotes for stock for last 5 years.
        :return: quotes of stock with Open, High, Low, Close, Volume, Timestamp
        """
        _to, _from = create_unix_timestamps(365 * 5)  # 5 years
        self._quotes_json = self.client.stock_candles(self._ticker, "D", _from, _to)

    def _transform_quotes_to_data_frame(self):
        """Transforms json quotes of stock into pandas DataFrame object.
        renaming columns, changing order, and transforming date timestamp to date
        :return:
        """
        data = pd.DataFrame(self._quotes_json)
        if data.empty:
            raise ValueError("The data frame with Quotes is empty!")
        data = rename_quotes_columns(data)
        data["Date"] = pd.to_datetime(data["Date"], unit="s").dt.date
        return data[["Date", "Open", "Low", "High", "Close", "Volume"]]

    def _transform_current_metrics_to_data_frame(self):
        current = pd.DataFrame(self._current_metrics_json.items())
        current.columns = ["KPI", "Value"]
        return current

    # Todo define which kpi can be useful to calculate some metrics for portfolio.

    def _transform_annual_metrics_to_data_frame(self):
        return pd.DataFrame.from_dict(self._annual_metrics_json, orient='index').transpose()


