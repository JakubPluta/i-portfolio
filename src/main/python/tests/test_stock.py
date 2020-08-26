from stock import Stock


def test_stock_should_be_created():
    # given
    ticker = "AMZN"

    # when
    stock = Stock(ticker)

    # then
    assert stock
    assert stock.client.api_key is not None
    assert isinstance(stock, Stock)
    assert stock._info is not None
