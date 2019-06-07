"""
@brief      test log(time=13s)
"""
import datetime
import os
import unittest
from pyquickhelper.pycode import ExtTestCase
from manydataapi.parsers.ct1 import dummy_ct1, read_ct1
from manydataapi.parsers.folders import read_folder


class TestCt1(ExtTestCase):

    exp = {'DATETIME': datetime.datetime(2011, 6, 5, 11, 30, 56),
           'FCODE': '5',
           'FCODE1': '00004',
           'FCODE2': '000107',
           'HT': 16.93,
           'INFO0': 'HASH2',
           'INFO1': '216',
           'INFO2': 'VERS',
           'INFO3': 'VERSION',
           'INFO4': 'CT100',
           'INFOL2': 'INFO',
           'INFOL2_1': '',
           'INFOL2_2': '',
           'INFOL2_3': '0',
           'INFOL2_4': '0',
           'INFO_': 'HASH1',
           'NAME': 'PERS1',
           'NB1': '0',
           'NB2': '4',
           'P0': '0',
           'PLACE': 'PLACE',
           'STREET': 'STREET',
           'TOTAL': 18.74,
           'TVA': 1.15,
           'ZIPCODE': 'ZIP',
           'data': [{'IT1': '0',
                     'IT10': '    0.00',
                     'IT2': '0',
                     'IT4': '0',
                     'IT5': '0',
                     'IT6': '      ',
                     'IT7': '0',
                     'IT8': '0',
                     'IT9': '   0.00',
                     'ITCODE': '800',
                     'ITNAME': 'ITEM11',
                     'ITPRICE': 5.25,
                     'ITQU': 0.2501,
                     'ITUNIT': 21.0,
                     'PIECE': False,
                     'TVA': 0.85,
                     'TVAID': '1',
                     'TVARATE': 5.5},
                    {'IT1': '0',
                     'IT10': '    0.00',
                     'IT2': '0',
                     'IT4': '0',
                     'IT5': '0',
                     'IT6': '      ',
                     'IT7': '0',
                     'IT8': '0',
                     'IT9': '   0.00',
                     'ITCODE': '605',
                     'ITNAME': 'ITEM17',
                     'ITPRICE': 7.28,
                     'ITQU': 0.4043,
                     'ITUNIT': 18.0,
                     'PIECE': False,
                     'TVA': 0.85,
                     'TVAID': '1',
                     'TVARATE': 5.5},
                    {'IT1': '0',
                     'IT10': '    0.00',
                     'IT2': '0',
                     'IT4': '0',
                     'IT5': '2',
                     'IT6': '      ',
                     'IT7': '0',
                     'IT8': '0',
                     'IT9': '   0.00',
                     'ITCODE': '102',
                     'ITNAME': 'ITEM19',
                     'ITPRICE': 3.4,
                     'ITQU': 2,
                     'ITUNIT': 1.7,
                     'PIECE': True,
                     'TVA': 0.85,
                     'TVAID': '1',
                     'TVARATE': 5.5},
                    {'IT1': '0',
                     'IT10': '    0.00',
                     'IT2': '0',
                     'IT4': '0',
                     'IT5': '2',
                     'IT6': '      ',
                     'IT7': '0',
                     'IT8': '0',
                     'IT9': '   0.00',
                     'ITCODE': '3',
                     'ITNAME': 'ITEM1',
                     'ITPRICE': 0.31,
                     'ITQU': 1,
                     'ITUNIT': 0.31,
                     'PIECE': True,
                     'TVA': 0.3,
                     'TVAID': '2',
                     'TVARATE': 20.0},
                    {'IT1': '0',
                     'IT10': '    0.00',
                     'IT2': '0',
                     'IT4': '0',
                     'IT5': '2',
                     'IT6': '      ',
                     'IT7': '0',
                     'IT8': '0',
                     'IT9': '   0.00',
                     'ITCODE': '4',
                     'ITNAME': 'ITEM2',
                     'ITPRICE': 2.5,
                     'ITQU': 1,
                     'ITUNIT': 2.5,
                     'PIECE': True,
                     'TVA': 0.3,
                     'TVAID': '2',
                     'TVARATE': 20.0}],
           'tva': [{'HT': 15.43,
                    'RATE': 5.5,
                    'TOTAL': 16.28,
                    'TVAID': '1',
                    'VALUE': 0.85},
                   {'HT': 1.5, 'RATE': 20.0, 'TOTAL': 1.8, 'TVAID': '2', 'VALUE': 0.3}]}

    def test_ct1(self):
        dummy = dummy_ct1()
        res = read_ct1(dummy, as_df=False)
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 4)
        obs = res[0]
        self.assertEqual(len(obs['data']), 5)
        self.assertEqual(TestCt1.exp, obs)

    def test_ct1_df(self):
        dummy = dummy_ct1()
        res = read_ct1(dummy, as_df=True)
        self.assertEqual(res.shape, (17, 42))

    def test_ct1_folder(self):
        dummy = dummy_ct1()
        fold = os.path.dirname(dummy)
        res1 = read_ct1(dummy, as_df=False)
        res2 = read_folder(fold, lambda f: read_ct1(f, as_df=False))
        self.assertEqual(res1, res2)

    def test_ct1_folder_ct1(self):
        dummy = dummy_ct1()
        fold = os.path.dirname(dummy)
        res1 = read_ct1(dummy, as_df=True)
        res2 = read_folder(fold)
        self.assertEqual(res1, res2)

    def test_ct1_folder_df(self):
        dummy = dummy_ct1()
        fold = os.path.dirname(dummy)
        res1 = read_ct1(dummy, as_df=True)
        res2 = read_folder(fold, lambda f: read_ct1(f, as_df=True))
        self.assertEqual(res1, res2)


if __name__ == "__main__":
    unittest.main()
