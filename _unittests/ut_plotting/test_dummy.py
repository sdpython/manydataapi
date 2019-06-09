"""
@brief      test log(time=13s)
"""
import unittest
from pyquickhelper.pycode import ExtTestCase
from manydataapi.plotting import plot_aggregated_ts, daily_timeseries


class TestDummm(ExtTestCase):

    def test_agg_raise(self):
        df = daily_timeseries()

        from matplotlib import pyplot as plt
        _, ax = plt.subplots(1, 1)
        plot_aggregated_ts(df, ax=ax, value='X', agg='year')
        plt.close('all')


if __name__ == "__main__":
    unittest.main()
