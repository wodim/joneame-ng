from random import randint

from flask import render_template, request

from joneame.database import db
from joneame.models import Quote


def get_random_quote():
    quote_max = (db.session.query(db.func.max(Quote.quote_id)).first()[0])
    quote = (
        Quote.query
        .filter(Quote.quote_id > randint(0, quote_max))
        .first()
    )

    return quote


def render_page(template, sidebar=None, submenu=None, show_quote=True,
                endpoint=None, toolbox=None, **kwargs):
    kwargs['random_quote'] = get_random_quote() if show_quote else None
    kwargs['sidebar'] = sidebar
    kwargs['submenu'] = submenu
    kwargs['toolbox'] = toolbox
    kwargs['endpoint'] = endpoint if endpoint else request.endpoint

    return render_template(template, **kwargs)
