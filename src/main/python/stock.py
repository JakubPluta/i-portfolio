from utils import *
import finnhub as fh
import os
import pandas as pd
from returns import *
from metrics import METRICS


api_key = os.environ.get("FH_API_KEY")

if not api_key:
    raise KeyError(
        "There is no API KEY for Finnhub\nPlease visit https://finnhub.io/docs/api to get your free api key"
    )


class Stock:

    client = fh.Client(api_key)

    def __init__(self, ticker):
        self.ticker = ticker
        self.quotes = self.get_quotes()
        self.metrics = self.get_current_metrics_df()
        self.company_info = self.get_company_info()
        self.expected_returns = self.calculate_expected_returns()
        self.volatility = self.calculate_volatility()
        self.daily_returns = self.calculate_daily_returns()
        self.log_daily_returns = self.calculate_daily_log_returns()

    # Public methods

    def get_quotes(self):
        """Transforms json quotes of stock into pandas DataFrame object.
        renaming columns, changing order, and transforming date timestamp to date
        :return:
        """
        quotes = self._get_quotes()
        data = pd.DataFrame(quotes)
        if data.empty:
            raise ValueError("The data frame with Quotes is empty!")
        data = rename_quotes_columns(data)
        data["Date"] = pd.to_datetime(data["Date"], unit="s").dt.date
        return data[["Date", "Close"]].set_index("Date")

    def get_current_metrics_df(self):
        metrics = self._get_metrics().items()
        current = pd.DataFrame(metrics)
        current.columns = ["KPI", "Value"]
        return current.fillna(0).set_index("KPI")

    def get_company_info(self):
        return pd.DataFrame(self._get_company_info().items())

    def calculate_daily_returns(self):
        return calculate_daily_returns(self.quotes)

    def calculate_daily_log_returns(self):
        return calculate_daily_logarithmic_returns(self.quotes)

    def calculate_expected_returns(self):
        return historical_mean_return(self.quotes)

    def calculate_volatility(self, trading_days=252):
        return self.calculate_daily_returns().values.std() * np.sqrt(trading_days)

    # Private methods

    def _get_company_info(self):
        """Get basic company information
        :return: json with company information
        """
        return self.client.company_profile(symbol=self.ticker)

    def _get_metrics(self):
        """Get financial metrics from Finnhub API
        :return: Financial Metrics for current year
        """
        metrics = self.client.company_basic_financials(self.ticker, "all")
        if metrics.get("metric"):
            return {kpi: metrics.get("metric")[kpi] for kpi in METRICS}

    def _get_quotes(self):
        """Get quotes for stock for last 5 years.
        :return: quotes of stock with Open, High, Low, Close, Volume, Timestamp
        """
        _to, _from = create_unix_timestamps(365 * 5)  # 5 years
        return self.client.stock_candles(self.ticker, "D", _from, _to)
