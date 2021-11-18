#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of Qt for Python.
##
## $QT_BEGIN_LICENSE:COMM$
##
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## $QT_END_LICENSE$
##
#############################################################################

from __future__ import print_function, absolute_import

"""
errorhandler.py

This module handles the TypeError messages which were previously
produced by the generated C code.

This version is at least consistent with the signatures, which
are created by the same module.

Experimentally, we are trying to guess those errors which are
just the wrong number of elements in an iterator.
At the moment, it is unclear whether the information given is
enough to produce a useful ValueError.

This matter will be improved in a later version.
"""

import sys

from shibokensupport.signature import inspect
from shibokensupport.signature import get_signature
from shibokensupport.signature.mapping import update_mapping, namespace
from textwrap import dedent


def qt_isinstance(inst, the_type):
    if the_type == float:
        return isinstance(inst, int) or isinstance(int, float)
    try:
        return isinstance(inst, the_type)
    except TypeError as e:
        print("FIXME", e)
        return False


def matched_type(args, sigs):
    for sig in sigs:
        params = list(sig.parameters.values())
        if len(args) > len(params):
            continue
        if len(args) < len(params):
            k = len(args)
            if params[k].default is params[k].empty:
                # this is a necessary parameter, so it fails.
                continue
        ok = True
        for arg, param in zip(args, params):
            ann = param.annotation
            if qt_isinstance(arg, ann):
                continue
            ok = False
        if ok:
            return sig
    return None


def seterror_argument(args, func_name, info):
    try:
        func = eval(func_name, namespace)
    except Exception as e:
        msg = "Error evaluating `{func_name}`: {e}".format(**locals())
        return type(e), msg
    if info and type(info) is str:
        err = TypeError
        if info == "<":
            msg = "{func_name}(): not enough arguments".format(**locals())
        elif info == ">":
            msg = "{func_name}(): too many arguments".format(**locals())
        elif info.isalnum():
            msg = "{func_name}(): got multiple values for keyword argument '{info}'".format(**locals())
        else:
            msg = "{func_name}(): {info}".format(**locals())
            err = AttributeError
        return err, msg
    if info and type(info) is dict:
        keyword = tuple(info)[0]
        msg = "{func_name}(): unsupported keyword '{keyword}'".format(**locals())
        return AttributeError, msg
    sigs = get_signature(func, "typeerror")
    if not sigs:
        msg = "{func_name}({args}) is wrong (missing signature)".format(**locals())
        return TypeError, msg
    if type(sigs) != list:
        sigs = [sigs]
    if type(args) != tuple:
        args = (args,)
    # temp!
    found = matched_type(args, sigs)
    if found:
        msg = dedent("""
            '{func_name}' called with wrong argument values:
              {func_name}{args}
            Found signature:
              {func_name}{found}
            """.format(**locals())).strip()
        return ValueError, msg
    type_str = ", ".join(type(arg).__name__ for arg in args)
    msg = dedent("""
        '{func_name}' called with wrong argument types:
          {func_name}({type_str})
        Supported signatures:
        """.format(**locals())).strip()
    for sig in sigs:
        msg += "\n  {func_name}{sig}".format(**locals())
    # We don't raise the error here, to avoid the loader in the traceback.
    return TypeError, msg

def check_string_type(s):
    if sys.version_info[0] == 3:
        return isinstance(s, str)
    else:
        return isinstance(s, (str, unicode))

def make_helptext(func):
    existing_doc = func.__doc__
    sigs = get_signature(func)
    if not sigs:
        return existing_doc
    if type(sigs) != list:
        sigs = [sigs]
    try:
        func_name = func.__name__
    except AttributeError:
        func_name = func.__func__.__name__
    sigtext = "\n".join(func_name + str(sig) for sig in sigs)
    msg = sigtext + "\n\n" + existing_doc if check_string_type(existing_doc) else sigtext
    return msg

# end of file
