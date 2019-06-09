"""
@file
@brief Dummy timeseries.
"""
from datetime import datetime, timedelta
from numpy.random import RandomState
from pandas import DataFrame


def daily_timeseries(start=None, end=None, seed=None):
    """
    Creates a random positive timeseries.

    @param      start   start date, 2 years from end if None
    @param      end     end date, today if None
    @param      seed    random seed
    @return             dataframe
    """
    if end is None:
        end = datetime.now()
    if start is None:
        start = end - timedelta(365 * 2)
    day = timedelta(1)
    rows = []
    while start <= end:
        rows.append(dict(date=start))
        start += day
    df = DataFrame(rows)
    state = RandomState(seed=seed)
    df["X"] = state.randn(df.shape[0])
    return df
