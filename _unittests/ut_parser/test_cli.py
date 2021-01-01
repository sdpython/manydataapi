"""
@brief      test log(time=13s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG, BufferedPrint
from pyquickhelper.pycode import ExtTestCase, get_temp_folder
from manydataapi.parsers.ct1 import dummy_ct1
from manydataapi.__main__ import main


class TestCli(ExtTestCase):

    def test_cli(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        st = BufferedPrint()
        main(args=["read_folder", "--help"], fLOG=st.fprint)
        res = str(st)
        self.assertIn("usage: read_folder", res)

        st = BufferedPrint()
        fold = os.path.dirname(dummy_ct1())
        temp = get_temp_folder(__file__, "temp_cli")
        dest = os.path.join(temp, "example.xlsx")
        main(args=["read_folder", "-f", fold, '-r', 'ct1',
                   '--out', dest], fLOG=st.fprint)
        res = str(st)
        self.assertExists(dest)


if __name__ == "__main__":
    unittest.main()
