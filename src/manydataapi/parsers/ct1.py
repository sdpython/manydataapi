# -*- coding:utf-8 -*-
"""
@file
@brief Parses format from a paying machine.
"""
import copy
import datetime
import os
import pprint


def dummy_ct1():
    """
    Returns a dummy file for format ``CT1``.

    .. runpython::
        :showcode:

        from manydataapi.parsers.ct1 import dummy_ct1()
        name = dummy_ct1()
        with open(name) as f:
            for i, line in enumerate(f):
                print(i, line)
                if i > 10:
                    break
    """
    this = os.path.dirname(__file__)
    data = os.path.join(this, "dummies", "DDMMYYXX.CT1")
    if not os.path.exists(data):
        raise FileNotFoundError(data)
    return data


def read_ct1(file_or_str, encoding='ascii', as_df=True):
    """
    Parses a file or a string which follows a specific
    format. See function @see fn dummy_ct1.

    @param      file_or_str     file or string
    @param      encoding        encoding
    @param      as_df           returns the results as a dataframe
    @return                     dataframe
    """
    if len(file_or_str) < 4000 and os.path.exists(file_or_str):
        with open(file_or_str, encoding=encoding) as f:
            content = f.read()

    def _post_process(rec):
        total = sum(obs['ITPRICE'] for obs in rec['data'])
        if abs(total - rec['TOTAL']) > 0.01:
            raise ValueError('Unexected total {} != {}\n{}'.format(
                rec['TOTAL'], total, pprint.pformat(rec)))
        if record['TOTAL-'] != rec['TOTAL']:
            raise ValueError("Mismatch total' {} != {}\n{}".format(
                rec['TOTAL'], record['TOTAL-'], pprint.pformat(record)))
        if record['TOTAL_'] != rec['TOTAL']:
            raise ValueError("Mismatch total' {} != {}\n{}".format(
                rec['TOTAL'], record['TOTAL_'], pprint.pformat(record)))
        del record['TOTAL_']
        del record['TOTAL-']
        tva_d = {t['TVAID']: t for t in record['tva']}
        for item in record['data']:
            tvaid = item['TVAID']
            item['TVARATE'] = tva_d[tvaid]['RATE']
            item['TVA'] = tva_d[tvaid]['VALUE']

    records = []
    record = None
    for i, line in enumerate(content.split('\n')):
        line = line.strip('\r')
        if line.startswith("\x02"):
            if record is not None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            record = dict(data=[], tva=[])
            spl = line[1:].split("\x1d")
            for ii, info in enumerate(spl):
                record['INFO%d' % ii] = info

        elif line.startswith('\x04'):
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line.strip("\x04\x05")
            record['INFO_'] = line  # pylint: disable=E1137
            records.append(record)  # pylint: disable=E1137
            record = None

        elif line.startswith('H\x1d'):
            # description
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[2:]
            spl = line.split("\x1d")
            names = ['NB1', 'NB2', 'NAME', 'PLACE', 'STREET', 'ZIPCODE',
                     'INFOL2', 'INFOL2_1', 'INFOL2_2', 'INFOL2_3', 'INFOL2_4']
            for n, v in zip(names, spl):
                record[n] = v  # pylint: disable=E1137

        elif line.startswith('L\x1d'):
            # items
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[2:]
            spl = line.split("\x1d")
            names = ['ITCODE', 'ITNAME', 'IT1', 'IT2', 'TVAID', 'IT4',
                     'ITUNIT', 'ITQU', 'IT5', 'ITPRICE',
                     'IT6', 'IT7', 'IT8', 'IT9', 'IT10', 'IT11', 'IT12']
            obs = {}
            for n, v in zip(names, spl):
                if n in ['ITUNIT', 'ITQU', 'ITPRICE']:
                    obs[n] = float(v)
                else:
                    obs[n] = v
            n = 'ITQU'
            if obs[n] < 0.01 and int(obs[n] * 1000) == obs[n] * 1000:
                obs['PIECE'] = True
                obs[n] = int(obs[n] * 1000)
            else:
                obs['PIECE'] = False
            diff = abs(obs['ITQU'] * obs['ITUNIT'] - obs['ITPRICE'])
            if diff >= 0.01:  # 1 cent
                raise ValueError("{} * {} = {} != {} at line {}\n{}\n{}".format(
                    obs['ITQU'], obs['ITUNIT'], obs['ITQU'] * obs['ITUNIT'],
                    obs['ITPRICE'], i + 1, obs, line))
            record['data'].append(obs)  # pylint: disable=E1136

        elif line.startswith('P\x1d'):
            # items
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[2:]
            spl = line.split("\x1d")
            names = ['P0', 'TOTAL', 'P2']
            for n, v in zip(names, spl):
                if n in ['TOTAL']:
                    record[n] = float(v)  # pylint: disable=E1137
                else:
                    record[n] = v  # pylint: disable=E1137

        elif line.startswith('T\x1d9\x1d'):
            # items
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[4:]
            spl = line.split("\x1d")
            names = ['HT', 'TVA', 'TOTAL_']
            tva = {}
            for n, v in zip(names, spl):
                record[n] = float(v)  # pylint: disable=E1137

        elif line.startswith('T\x1d'):
            # items
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[2:]
            spl = line.split("\x1d")
            names = ['TVAID', 'RATE', 'HT', 'VALUE', 'TOTAL']
            tva = {}
            for n, v in zip(names, spl):
                if n == 'TVAID':
                    tva[n] = v
                else:
                    try:
                        tva[n] = float(v)
                    except ValueError:
                        tva[n] = v
            record['tva'].append(tva)  # pylint: disable=E1136

        elif line.startswith('F\x1d'):
            # items
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[2:]
            spl = line.split("\x1d")
            names = ['FCODE', 'TOTAL-', 'DATE', 'TIME', 'FCODE1', 'FCODE2']
            for n, v in zip(names, spl):
                if n in {'TOTAL-', }:
                    record[n] = float(v)  # pylint: disable=E1137
                elif n == "TIME":
                    vtime = v
                elif n == "DATE":
                    vdate = v
                else:
                    record[n] = v  # pylint: disable=E1137
            record["DATETIME"] = datetime.datetime.strptime(  # pylint: disable=E1137
                "{} {}".format(vdate, vtime), "%d.%m.%Y %H:%M:%S")

    # verification
    for record in records:
        _post_process(record)

    if as_df:
        new_records = []
        for record in records:
            rec = copy.deepcopy(record)
            del rec['tva']
            data = rec['data']
            del rec['data']
            for d in data:
                d.update(rec)
                new_records.append(d)
        import pandas
        return pandas.DataFrame(new_records)
    else:
        return records
