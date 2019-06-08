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
        rec['TOTAL'] = total
        if abs(record['TOTAL-'] - rec['TOTAL']) >= 0.01:
            raise ValueError("Mismatch total' {} != {}".format(
                rec['TOTAL'], record['TOTAL-']))
        if abs(record['TOTAL_'] - rec['TOTAL']) >= 0.01:
            raise ValueError("Mismatch total' {} != {}".format(
                rec['TOTAL'], record['TOTAL_']))
        del record['TOTAL_']
        del record['TOTAL-']
        tva_d = {t['TVAID']: t for t in record['tva']}
        for item in record['data']:
            tvaid = item['TVAID']
            item['TVARATE'] = tva_d[tvaid]['RATE']
            item['TVA'] = tva_d[tvaid]['VALUE']
        if len(record["data"]) == 0:
            raise ValueError("No record.")

    records = []
    record = None
    first_line = None
    content_ = content.split('\n')
    for i, line in enumerate(content_):
        line = line.strip('\r')
        if line.startswith("\x02"):
            if record is not None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            record = dict(data=[], tva=[])
            spl = line[1:].split("\x1d")
            for ii, info in enumerate(spl):
                record['INFO%d' % ii] = info
            first_line = i

        elif line.startswith('\x04'):
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line.strip("\x04\x05")
            record['INFO_'] = line  # pylint: disable=E1137

            # verification
            if len(record['data']) > 0:  # pylint: disable=E1136
                try:
                    _post_process(record)
                except (KeyError, ValueError) as e:
                    raise ValueError("Unable to process one record line {}-{}\n{}\n-\n{}".format(
                        first_line + 1, i + 1, pprint.pformat(record),
                        "\n".join(content_[first_line: i + 1]))) from e

                records.append(record)  # pylint: disable=E1137

            first_line = None
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
                     'ITUNIT', 'ITQU', 'CAT', 'ITPRICE',
                     'IT6', 'NEG', 'IT8', 'IT9', 'IT10', 'IT11', 'IT12']
            obs = {}
            for n, v in zip(names, spl):
                if n in ['ITUNIT', 'ITQU', 'ITPRICE', 'NEG', 'CAT']:
                    obs[n] = float(v.replace(" ", ""))
                else:
                    obs[n] = v
            n = 'ITQU'
            if obs['CAT'] == 2:
                obs['PIECE'] = True
                obs[n] = int(obs[n] * 1000)
            else:
                obs['PIECE'] = False
            if obs['NEG']:
                obs['ITUNIT'] *= -1
                obs['ITPRICE'] *= -1
            diff = abs(obs['ITQU'] * obs['ITUNIT'] - obs['ITPRICE'])
            if diff >= 0.01:  # 1 cent
                obs['ERROR'] = diff
                if obs['ITQU'] == 0 and obs['ITUNIT'] == 0:
                    obs['ERROR'] = 0.
                    obs['WHY'] = True
                    obs['ITPRICE'] = 0.
                elif diff >= 0.1:
                    raise ValueError("{} * {} = {} != {} at line {}\n{}\n{}".format(
                        obs['ITQU'], obs['ITUNIT'], obs['ITQU'] * obs['ITUNIT'],
                        obs['ITPRICE'], i + 1, obs, line))
            record['data'].append(obs)  # pylint: disable=E1136

        elif line.startswith('T\x1d9\x1d'):
            # items
            if record is None:
                raise RuntimeError("Wrong format at line {}".format(i + 1))
            line = line[4:]
            spl = line.split("\x1d")
            names = ['HT', 'TVA', 'TOTAL_']
            tva = {}
            for n, v in zip(names, spl):
                record[n] = float(v.replace(" ", ""))  # pylint: disable=E1137

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
                        tva[n] = float(v.replace(" ", ""))
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
            vtime = None
            vdate = None
            for n, v in zip(names, spl):
                if n in {'TOTAL-', }:
                    record[n] = float(v.replace(" ", "")  # pylint: disable=E1137
                                      )  # pylint: disable=E1137
                elif n == "TIME":
                    vtime = v
                elif n == "DATE":
                    vdate = v
                else:
                    record[n] = v  # pylint: disable=E1137
            record["DATETIME"] = datetime.datetime.strptime(  # pylint: disable=E1137
                "{} {}".format(vdate, vtime), "%d.%m.%Y %H:%M:%S")

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
