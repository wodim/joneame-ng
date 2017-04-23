from random import randint

from flask import render_template

from joneame.database import db
from joneame.models import QuoteModel


def get_random_quote():
    quote_max = (db.session.query(db.func.max(QuoteModel.quote_id)).first()[0])
    quote = (
        QuoteModel.query
        .filter(QuoteModel.quote_id > randint(0, quote_max))
        .first()
    )

    return quote


def render_page(template, sideboxes=None, show_quote=True, **kwargs):
    if show_quote:
        kwargs['random_quote'] = get_random_quote()

    return render_template(template, **kwargs)
