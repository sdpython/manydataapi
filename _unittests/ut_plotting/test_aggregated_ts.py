"""
@brief      test log(time=3s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from manydataapi.parsers.ct1 import dummy_ct1, read_ct1
from manydataapi.plotting import plot_aggregated_ts


class TestAggregatedTs(ExtTestCase):

    def test_agg_raise(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        self.assertRaise(lambda: plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='year_'),
                         ValueError)
        plt.close('all')

    def test_agg_year(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='year')
        plt.close('all')

    def test_agg_month(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='month')
        plt.close('all')

    def test_agg_day(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='day')
        plt.close('all')

    def test_agg_weekday(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='weekday')
        plt.close('all')

    def test_agg_hour(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='hour')
        plt.close('all')

    def test_agg_week_hours(self):
        dummy = dummy_ct1()
        df = read_ct1(dummy, as_df=True)

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='ITPRICE', agg='weekhour')
        plt.close('all')


if __name__ == "__main__":
    unittest.main()
