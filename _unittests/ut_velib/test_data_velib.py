"""
@brief      test log(time=28s)
"""
import os
import unittest
import datetime
import warnings
import pandas
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import is_travis_or_appveyor, get_temp_folder, ExtTestCase
from manydataapi.velib import DataCollectJCDecaux


class TestDataJCDecaux(ExtTestCase):

    def get_private_key(self):
        """
        retrive the key, this key is private and must not be shared through the source

        look at the code to see where I chose to put this key not shared in this file
        """
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            import keyring
        try:
            key = keyring.get_password("velib", "manydataapi,key")
        except RuntimeError:
            key = None
        if not is_travis_or_appveyor() and key is None:
            raise ValueError("unable to retrieve API key")
        return key

    def test_datetime(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")
        f = 1368121860000.0
        d = datetime.datetime.fromtimestamp(f / 1000)
        if d != datetime.datetime(2013, 5, 9, 19, 51, 0):
            # issue with time (not the same local)
            if d.year != 2013 and d.month != 5 and d.day != 9:
                raise AssertionError("difference: " + str(d))

    def test_data_velib_json(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")

        tempfold = get_temp_folder(__file__, "temp_data_i")
        temp_file = os.path.join(tempfold, "data_velib.txt")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        self.assertTrue(not os.path.exists(temp_file))

        key = self.get_private_key()
        if key is None:
            return

        velib = DataCollectJCDecaux(key)
        # Paris changed velib's owner (2018-01).
        js = velib.get_json("besancon")

        self.assertIsInstance(js, list)
        fLOG(type(js))
        nb = 0
        for o in js:
            fLOG(o)
            nb += 1
            if nb > 10:
                break
        self.assertGreater(nb, 0)
        self.assertGreater(len(js), 0)

        tbl = pandas.DataFrame(js)
        tbl.to_csv(temp_file, sep="\t")
        self.assertExists(temp_file)
        fLOG(tbl[:10])

    def test_data_velib_json_collect(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")

        tempfold = get_temp_folder(__file__, "temp_data_i2")
        temp_file = os.path.join(tempfold, "data_velib.txt")

        delay = datetime.timedelta(seconds=5)
        dt = datetime.datetime.now() + delay

        key = self.get_private_key()
        if key is None:
            return

        velib = DataCollectJCDecaux(key)
        velib.collecting_data("nancy", 1000, temp_file, stop_datetime=dt,
                              log_every=1, fLOG=fLOG)

        if not os.path.exists(temp_file):
            raise FileNotFoundError(temp_file)
        with open(temp_file, "r", encoding="utf8") as f:
            lines = f.readlines()
        if len(lines) < 1:
            raise AssertionError(
                "len(lines)<1: %d\n%s" %
                (len(lines), "\n".join(lines)))
        self.assertLesser(len(lines), 10)
        self.assertIn("\t", lines[0])

        dt = datetime.datetime.now() + delay
        velib.collecting_data("nancy", 1000, temp_file, stop_datetime=dt,
                              single_file=False, log_every=1, fLOG=fLOG)
        res = os.listdir(tempfold)
        if len(res) <= 2:
            raise AssertionError(str(res))

    def test_data_velib_json_collect_func(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")

        tempfold = get_temp_folder(__file__, "temp_data_func")
        temp_file = os.path.join(tempfold, "data_velib.txt")

        delay = datetime.timedelta(seconds=5)
        dt = datetime.datetime.now() + delay

        key = self.get_private_key()
        if key is None:
            return

        # Paris changed velib's owner (2018-01)
        DataCollectJCDecaux.run_collection(key, contract="nancy", delayms=1000,
                                           folder_file=temp_file, single_file=True,
                                           stop_datetime=dt, log_every=1, fLOG=fLOG)

        if not os.path.exists(temp_file):
            raise FileNotFoundError(temp_file)
        with open(temp_file, "r", encoding="utf8") as f:
            lines = f.readlines()
        if len(lines) < 1:
            raise AssertionError(
                "len(lines)<1: %d\n%s" %
                (len(lines), "\n".join(lines)))
        self.assertLesser(len(lines), 10)
        self.assertIn("\t", lines[0])

    def test_data_velib_json_collect_func_besancon(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")

        tempfold = get_temp_folder(__file__, "temp_data_func_bes")
        temp_file = os.path.join(tempfold, "data_velib.txt")

        delay = datetime.timedelta(seconds=5)
        dt = datetime.datetime.now() + delay

        key = self.get_private_key()
        if key is None:
            return

        DataCollectJCDecaux.run_collection(key, contract="besancon", delayms=1000,
                                           folder_file=temp_file, single_file=True,
                                           stop_datetime=dt, log_every=1, fLOG=fLOG)

        if not os.path.exists(temp_file):
            raise FileNotFoundError(temp_file)
        with open(temp_file, "r", encoding="utf8") as f:
            lines = f.readlines()
        if len(lines) < 1:
            raise AssertionError(
                "len(lines)<1: %d\n%s" %
                (len(lines), "\n".join(lines)))
        self.assertLesser(len(lines), 10)
        self.assertIn("\t", lines[0])

    def test_data_velib_contract(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__",
            LogFile="temp_hal_log2.txt")

        key = self.get_private_key()
        if key is None:
            return

        velib = DataCollectJCDecaux(key)
        cont = velib.get_contracts()
        # fLOG("**", cont)
        self.assertGreater(len(cont), 0)


if __name__ == "__main__":
    unittest.main()
