"""
@file
@brief Helpers about dataframe.
"""
import os


def dataframe_to(df, out, **kwargs):
    """
    Exports a dataframe into the write format.
    The function uses the file extension to choose the
    right exporter.

    @param      df      dataframe
    @param      out     filename
    @param      kwargs  additional parameter to the exporter
    """
    if isinstance(out, str):
        ext = os.path.splitext(out)[-1][1:]
        if ext == 'xlsx':
            ext = 'excel'
        meth = "to_" + ext
        if hasattr(df, meth):
            m = getattr(df, meth)
            m(out, **kwargs)
        else:
            raise RuntimeError("Method '{}' does not exist in type {}.".format(
                meth, type(df)))
    else:
        raise TypeError("out must be a string.")
