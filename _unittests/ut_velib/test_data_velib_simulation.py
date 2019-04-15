"""
@brief      test log(time=28s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from manydataapi.velib import DataCollectJCDecaux


class TestDataVelibSimulation (unittest.TestCase):

    def test_data_velib_simulation(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        fold = os.path.abspath(os.path.split(__file__)[0])
        data = os.path.join(fold, "data")

        for speed in (10, 15):
            for bike in (1, 2, 3, 5, 10):
                df = DataCollectJCDecaux.to_df(data)
                dfp, dfs = DataCollectJCDecaux.simulate(
                    df, bike, speed, fLOG=fLOG)

                dfp.to_csv(
                    "out_simul_bike_nb{0}_sp{1}_path.txt".format(
                        bike,
                        speed),
                    sep="\t",
                    index=False)
                dfs.to_csv(
                    "out_simul_bike_nb{0}_sp{1}_data.txt".format(
                        bike,
                        speed),
                    sep="\t",
                    index=False)
                if __name__ != "__main__":
                    return


if __name__ == "__main__":
    unittest.main()
