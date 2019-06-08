"""
@file
@brief Common plots for timeseries.
"""
import numpy


def get_index_date(df):
    """
    Returns the only column date.
    Raises an exception otherwise.

    @param      df      dataframe
    @return             column name
    """
    df = df.select_dtypes(include=[numpy.datetime64])
    if df.shape[1] != 1:
        raise RuntimeError("Unable to find a single column date in {}.".format(
            list(zip(df.columns, df.dtypes))))
    return df.columns[0]


def get_new_column(df, name):
    """
    Get a new column which does not exists in df.

    @param      name        suggestion
    """
    while name in df.columns:
        name += "_"
    return name


def plot_aggregated_ts(df, value, date=None, agg="month", ax=None):
    """
    Plots a, aggregated time series by a period of time.

    @param      df      dataframe
    @param      value   column to show
    @param      date    column to use as a date,
                        if None, it assume there is one and only one
    @param      agg     aggregation by ``'month'``, ``'day'``,
                        ``'year'``, ``'weekday'``
    @param      ax      existing ax
    @return             ax
    """
    if not ax:
        import matplotlib.pyplot as plt
        ax = plt.gca()
    if date is None:
        date = get_index_date(df)
    df = df[[date, value]].copy()
    if agg == "month":
        col1 = get_new_column(df, 'month')
        df[col1] = df[date].dt.month
        col2 = get_new_column(df, 'year')
        df[col2] = df[date].dt.year
        key = (col2, col1)
    elif agg == 'year':
        col2 = get_new_column(df, 'year')
        df[col2] = df[date].dt.year
        key = col2
    elif agg == 'day':
        col1 = get_new_column(df, 'month')
        df[col1] = df[date].dt.month
        col2 = get_new_column(df, 'year')
        df[col2] = df[date].dt.year
        col3 = get_new_column(df, 'day')
        df[col3] = df[date].dt.day
        key = (col2, col1, col3)
    elif agg == 'weekday':
        col1 = get_new_column(df, 'weekday')
        df[col1] = df[date].dt.month
        key = col1
    else:
        raise ValueError("Unknown aggregation '{}'.".format(agg))
    gr = df.groupby(key).sum()
    gr.plot(kind="bar", ax=ax)
    return ax
