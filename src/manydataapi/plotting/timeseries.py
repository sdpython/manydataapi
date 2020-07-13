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
        raise RuntimeError(  # pragma: no cover
            "Unable to find a single column date in {}.".format(
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


def plot_aggregated_ts(df, value, date=None, agg="month", ax=None,
                       kind='bar', **kwargs):
    """
    Plots a, aggregated time series by a period of time.

    @param      df      dataframe
    @param      value   column to show
    @param      date    column to use as a date,
                        if None, it assume there is one and only one
    @param      agg     aggregation by ``'month'``, ``'day'``,
                        ``'year'``, ``'weekday'``, ``'hour'``,
                        ``weekhour'``
    @param      kind    graph style
    @param      ax      existing ax
    @param      kwargs  additional parameter for the graph
    @return             ax

    .. plot::

        import matplotlib.pyplot as plt
        from manaydataapi.timeseries import plot_aggregated_ts, daily_timeseries
        df = plot_aggregated_ts()
        plot_aggregated_ts(df, value='X', agg='month')
        plt.show()
    """
    if not ax:
        import matplotlib.pyplot as plt  # pragma: no cover
        ax = plt.gca()  # pragma: no cover
    if date is None:
        date = get_index_date(df)
    df = df[[date, value]].copy()

    if agg == 'weekhour':
        col1 = get_new_column(df, 'weekday')
        df[col1] = df[date].dt.weekday
        col2 = get_new_column(df, 'hour')
        df[col2] = df[date].dt.hour
        key = [col2, col1]
        vals = [_ for _ in sorted(set(df[col1])) if not numpy.isnan(_)]
        for v in vals:
            gr = df[df[col1] == v].drop(col1, axis=1).groupby(col2).sum()
            gr.columns = ['wk=%d' % v]
            gr.plot(kind=kind, ax=ax, **kwargs)
    else:
        if agg == "month":
            col1 = get_new_column(df, 'month')
            df[col1] = df[date].dt.month
            col2 = get_new_column(df, 'year')
            df[col2] = df[date].dt.year
            key = [col2, col1]
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
            key = [col2, col1, col3]
        elif agg == 'weekday':
            col1 = get_new_column(df, 'weekday')
            df[col1] = df[date].dt.weekday
            key = col1
        elif agg == 'hour':
            col1 = get_new_column(df, 'hour')
            df[col1] = df[date].dt.hour
            key = col1
        else:
            raise ValueError("Unknown aggregation '{}'.".format(agg))
        gr = df.groupby(key).sum()
        gr.plot(kind=kind, ax=ax, **kwargs)
    return ax
