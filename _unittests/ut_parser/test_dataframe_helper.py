"""
@brief      test log(time=13s)
"""
import os
import unittest
import pandas
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from manydataapi.parsers import dataframe_to


class TestDataFrameHelper(ExtTestCase):

    def test_to_csv(self):
        df = pandas.DataFrame([dict(a='a', b=1)])
        temp = get_temp_folder(__file__, "temp_to_csv")
        name = os.path.join(temp, "df.csv")
        dataframe_to(df, name)
        self.assertExists(name)
        name = os.path.join(temp, "df.rrr")
        self.assertRaise(lambda: dataframe_to(df, name), RuntimeError)
        self.assertRaise(lambda: dataframe_to(df, None), TypeError)


if __name__ == "__main__":
    unittest.main()
