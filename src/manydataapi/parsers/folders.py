# -*- coding:utf-8 -*-
"""
@file
@brief Parses format from a paying machine.
"""
import re
import os
from .dataframe_helper import dataframe_to


def read_folder(folder=".", reader="CT1", pattern=".*[.].{1,3}$",
                verbose=False, out=None, fLOG=None):
    """
    Applies the same parser on many files in a folder.

    :param folder: folder
    :param reader: reader name or function which processes
        a string or a filename, possible read name: `CT1`.
    :param pattern: file pattern
    :param verbose: to show progress, it requires module :epkg:`tqdm`
    :param out: output the dataframe in a file
    :param fLOG: logging function
    :return: concatenated list or DataFrame

    The function is also available through a command line.

   .. cmdref::
        :title: Parses and merges files in a dictionary with format CT1
        :cmd: -m manydataapi read_folder --help
    """
    if isinstance(reader, str):
        if reader.lower() == 'ct1':
            from .ct1 import read_ct1

            def reader_(name):
                return read_ct1(name, as_df=True)
            reader = reader_
        else:
            raise ValueError(  # pragma: no cover
                "Unknown parser '{}'.".format(reader))

    if verbose and fLOG:
        fLOG("look into '%s'." % folder)
    names = []
    pat = re.compile(pattern)
    for name in os.listdir(folder):
        if pat.search(name):
            names.append(name)
    if len(names) == 0:
        raise FileNotFoundError(  # pragma: no cover
            "Unable to find file in '{}' following pattern '{}'.".format(
                folder, pattern))
    objs = []

    if verbose:
        from tqdm import tqdm  # pragma: no cover
        loop = tqdm(names)  # pragma: no cover
    else:
        loop = iter(names)

    for name in loop:
        try:
            obj = reader(os.path.join(folder, name))
        except (ValueError, KeyError) as e:  # pragma: no cover
            raise ValueError("Unable to parse file '{}'.".format(name)) from e
        objs.append(obj)

    if isinstance(objs[0], list):
        res = []
        for obj in objs:
            res.extend(obj)
        return res
    from pandas import DataFrame, concat
    if isinstance(objs[0], DataFrame):
        df = concat(objs, sort=False)
        if out is not None:
            dataframe_to(df, out)
            if verbose and fLOG:
                fLOG("wrote '%s'." % out)
        return df
    raise TypeError(  # pragma: no cover
        "Unable to merge type {}.".format(type(objs[0])))
