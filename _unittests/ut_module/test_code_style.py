"""
@brief      test log(time=0s)
"""
import os
import unittest
from pyquickhelper.loghelper import fLOG
from pyquickhelper.pycode import check_pep8, ExtTestCase


class TestCodeStyle(ExtTestCase):
    """Test style."""

    def test_style_src(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        src_ = os.path.normpath(os.path.join(thi, "..", "..", "src"))
        check_pep8(src_, fLOG=fLOG,
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'R1702', 'W0212', 'W0201'),
                   skip=["Class 'DataCollectJCDecaux' has no 'velib_get_key'",
                         "Redefining built-in 'iter'",
                         "data_jcdecaux.py:597: W0612",
                         "data_jcdecaux.py:465: W0612",
                         "data_jcdecaux.py:457: W0612",
                         "data_jcdecaux.py:457: W0612",
                         "data_jcdecaux.py:435: W0612",
                         "data_jcdecaux.py:435: W0612",
                         "data_jcdecaux.py:302: W0123",
                         "linkedin_access.py:302: E1123",
                         "linkedin_access.py:302: E1123",
                         "linkedin_access.py:302: E1123",
                         "linkedin_access.py:155: R1710",
                         "linkedin_access.py:239: E1101",
                         "linkedin_access.py:236: E1101",
                         "linkedin_access.py:214: E1101",
                         "linkedin_access.py:260: E1101",
                         ])

    def test_style_test(self):
        thi = os.path.abspath(os.path.dirname(__file__))
        test = os.path.normpath(os.path.join(thi, "..", ))
        check_pep8(test, fLOG=fLOG, neg_pattern="temp_.*",
                   pylint_ignore=('C0103', 'C1801', 'R0201', 'R1705', 'W0108', 'W0613',
                                  'C0111', 'W0703'),
                   skip=["src' imported but unused",
                         "skip_' imported but unused",
                         "skip__' imported but unused",
                         "skip___' imported but unused",
                         "Unused variable 'skip_'",
                         "imported as skip_",
                         "Unused import src",
                         "Redefining built-in 'iter'",
                         ])


if __name__ == "__main__":
    unittest.main()
