import datetime, time


def create_unix_timestamps(days=365):
    """
    :param days: number of days
    :return:
        * Today date converted to unix timestamp,
        * Today - number of days converted to unix timestamp
    """
    today = datetime.date.today()
    unixtime_today = time.mktime(today.timetuple())
    years_before = today - datetime.timedelta(days=days)
    unix_time_before = time.mktime(years_before.timetuple())
    return int(unixtime_today), int(unix_time_before)


def create_time_period_in_ymd_format(days=365):
    today = datetime.date.today().strftime("%Y-%m-%d")
    year_before = datetime.date.today() - datetime.timedelta(days)
    year_before = year_before.strftime("%Y-%m-%d")
    return today, year_before


def rename_quotes_columns(data):
    names = {
        "c": "Close",
        "o": "Open",
        "h": "High",
        "l": "Low",
        "t": "Date",
        "v": "Volume",
        "s": "Status",
    }
    try:
        return data.rename(columns=names)
    except KeyError:
        return data.reset_index().rename(columns=names)


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


