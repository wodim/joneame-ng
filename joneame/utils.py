import datetime
from urllib.parse import urlparse, urljoin

from flask import request
from flask_babel import _, format_datetime


def flatten(items, param):
    """Flattens a list of objects into a dict which will use a specific attrib
        as a key. This is, it turns this:
            [(attr1: val1, attr2: val2, param: 123),
             (attr1: val1, attr2: val2, param: 123),
             (attr1: val1, attr2: val2, param: 456),
             (attr1: val1, attr2: val2, param: 456),
             (attr1: val1, attr2: val2, param: 789)]
        Into this:
            {123: [(attr1: val1, attr2: val2, param: 123),
                   (attr1: val1, attr2: val2, param: 123)],
             456: [(attr1: val1, attr2: val2, param: 456),
                   (attr1: val1, attr2: val2, param: 456)],
             789: [(attr1: val1, attr2: val2, param: 789)]}"""
    output = {}
    for item in items:
        value = getattr(item, param)
        if value in output:
            output[value].append(item)
        else:
            output[value] = [item]
    return output


# originally from reddit
def format_dt(dt, sep=' '):
    s = (datetime.datetime.now() - dt).total_seconds()
    if s > (7*60*60*24):  # 7 days
        return format_datetime(dt)

    ret = []
    if s < 0:
        neg = True
        s *= -1
    else:
        neg = False

    if s >= (24*60*60):
        days = int(s//(24*60*60))
        ret.append('%dd' % days)
        s -= days*(24*60*60)
    if s >= 60*60:
        hours = int(s//(60*60))
        ret.append('%dh' % hours)
        s -= hours*(60*60)
    if s >= 60:
        minutes = int(s//60)
        ret.append('%dm' % minutes)
        s -= minutes*60
    if s >= 1:
        seconds = int(s)
        ret.append('%ds' % seconds)
        s -= seconds

    if not ret:
        return '0s'

    return ('-' if neg else '') + _('%(ret)s ago', ret=sep.join(ret))


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ('http', 'https') and
            ref_url.netloc == test_url.netloc)
