from datetime import datetime, timedelta
import re
from urllib.parse import urlparse, urljoin

from flask import request, url_for
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
    s = (datetime.now() - dt).total_seconds()
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


# from akari
def ellipsis(text, max_length):
    if len(text) > max_length:
        return text[:max_length] + '…'
    return text


# from fw
def html_escape(text):
    return text.replace('&', '&amp;') \
               .replace('<', '&lt;') \
               .replace('>', '&gt;')


def html_unescape(text):
    return text.replace('&amp;', '&') \
               .replace('&lt;', '<') \
               .replace('&gt;', '>')


rx_whitespace = re.compile(r'[ \t]{2,}')
rx_padding_ws = re.compile(r'^[ \t]*|[ \t]*$', re.MULTILINE)
rx_padding_newline = re.compile(r'^\n*|\n*$')
rx_newline_spam = re.compile('\n{3,}')
rx_link = re.compile(r'(https?://[a-z0-9\.\-_\?=&,/;%#:!\+]+)', re.M | re.I)
rx_link_fmt = '<a href="{href}" class="external">{link}</a>'
rx_mention = re.compile(r'\B@([a-z][a-z0-9\-_\.]+(,\d+)?)', re.I)
rx_mention_fmt = '<a href="{href}">@{user_login}</a>'
rx_bold = re.compile(r'\B(\*(\S+)\*)\B')
rx_bold_fmt = r'<strong>\2</strong>'
rx_italic = re.compile(r'\B(_(\S+)_)\B')
rx_italic_fmt = r'<em>\2</em>'
rx_del = re.compile(r'\B(\-(\S+)\-)\B')
rx_del_fmt = r'<del>\2</del>'


def rx_link_func(matchobj):
    link = matchobj.group(1)
    href = html_unescape(link)
    link = ellipsis(link, 70)
    return rx_link_fmt.format(href=href, link=link)


def rx_mention_func(matchobj):
    mention = matchobj.group(1)
    user_login, sep, post_id = mention.partition(',')
    if post_id:
        href = url_for('Post:get', user_login=user_login, post_id=post_id)
    else:
        href = url_for('User:get', user_login=user_login)
    return rx_mention_fmt.format(href=href, user_login=user_login)


def format_post_text(text):
    """takes text from the database, which is not cleaned up when stored,
        and prepares/escapes it to be shown inside a post. removes stupid
        whitespace/newlines and shows quoted text in green"""

    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '')
    text = rx_whitespace.sub(' ', text)
    text = rx_padding_ws.sub('', text)
    text = rx_padding_newline.sub('', text)
    text = rx_newline_spam.sub('\n\n', text)

    # safe beginning here
    text = html_escape(text)
    text = rx_mention.sub(rx_mention_func, text)
    text = rx_bold.sub(rx_bold_fmt, text)
    text = rx_italic.sub(rx_italic_fmt, text)
    text = rx_del.sub(rx_del_fmt, text)
    text = rx_link.sub(rx_link_func, text)
    text = text.replace('\n', '<br>\n')

    return text
# end fw


# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (test_url.scheme in ('http', 'https') and
            ref_url.netloc == test_url.netloc)


v_to_r = {'24h': timedelta(hours=24),
          '48h': timedelta(hours=48),
          '1w':  timedelta(weeks=1),
          '1m':  timedelta(weeks=4),
          '1y':  timedelta(days=365)}


def arg_to_timedelta(arg):
    """turns an argument (such as 24h) to a timedelta"""
    if arg and arg in v_to_r:
        return v_to_r[arg]
