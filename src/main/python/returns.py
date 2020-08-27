import pandas as pd
import numpy as np


def calculate_daily_returns(data: pd.DataFrame):
    return data.pct_change().dropna(how="all")


def calculate_mean_daily_returns(data):
    return data.mean()


def calculate_std_of_returns(data):
    return data.std()


def calculate_daily_logarithmic_returns(data: pd.DataFrame):
    return np.log(1 + data.pct_change()).dropna(how="all")


def __calculate_daily_logarithmic_returns(data: pd.DataFrame):
    return np.log(data / data.shift(1))


def historical_mean_return(data: pd.DataFrame, trading_days=252):
    return calculate_daily_returns(data).mean() * trading_days


def calculate_sharpe_ratio(returns, risk_free_rate, trading_days=252):
    """Sharpe ratio = (Mean return − Risk-free rate) / Standard deviation of return
    :return:
    """
    volatility = returns.std() * np.sqrt(trading_days)
    sharpe_ratio = (returns.mean() - risk_free_rate) / volatility
    return sharpe_ratio

