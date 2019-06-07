# -*- coding:utf-8 -*-
"""
@file
@brief Parses format from a paying machine.
"""
import re
import os


def read_folder(folder=".", reader="CT1", pattern=".*[.].{1,3}$"):
    """
    Applies the same parser on many files in a folder.

    @param      folder      folder
    @param      reader      reader name or function which processes a string or a filename,
                            possible read name: `CT1`.
    @param      pattern     file pattern
    @return                 concatenated list or DataFrame
    """
    if isinstance(reader, str):
        if reader.lower() == 'ct1':
            from .ct1 import read_ct1

            def reader_(name):
                return read_ct1(name, as_df=True)
            reader = reader_
        else:
            raise ValueError("Unknown parser '{}'.".format(reader))

    names = []
    pat = re.compile(pattern)
    for name in os.listdir(folder):
        if pat.search(name):
            names.append(name)
    if len(names) == 0:
        raise FileNotFoundError(
            "Unable to find file in '{}' following pattern '{}'.".format(folder, pattern))
    objs = []
    for name in names:
        try:
            obj = reader(os.path.join(folder, name))
        except ValueError as e:
            raise ValueError("Unable to parse file '{}'.".format(name)) from e
        objs.append(obj)

    if isinstance(objs[0], list):
        res = []
        for obj in objs:
            res.extend(obj)
        return res
    else:
        from pandas import DataFrame, concat
        if isinstance(objs[0], DataFrame):
            return concat(objs)
        else:
            raise TypeError("Unable to merge type {}.".format(type(objs[0])))
