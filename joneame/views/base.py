from random import randint

from flask import render_template, request

from joneame.config import _cfgi
from joneame.database import db
from joneame.models import Quote


def paginate(items, page_size=None):
    page = request.args.get('page', 1, type=int)
    page_size = page_size or _cfgi('misc', 'page_size')

    return items.paginate(page, page_size)


def build_pagination_args(pagination, submenu):
    args = {}
    if submenu and submenu.default_hint in request.args:
        args.update({submenu.default_hint: request.args[submenu.default_hint]})
    args.update(dict(request.view_args))
    return args


def get_random_quote():
    quote_max = db.session.query(db.func.max(Quote.quote_id)).first()[0]
    quote = (
        Quote.query
        .filter(Quote.quote_id > randint(0, quote_max))
        .options(db.joinedload(Quote.user))
        .first()
    )

    return quote


def render_page(template, sidebar=None, submenu=None, show_quote=True,
                endpoint=None, toolbox=None, pagination=None, **kwargs):
    kwargs.update({
        'random_quote': get_random_quote() if show_quote else None,
        'sidebar': sidebar, 'submenu': submenu, 'toolbox': toolbox,
        'endpoint': endpoint or request.endpoint, 'pagination': pagination
    })
    if pagination:
        kwargs['pagination'] = pagination
        kwargs['pagination'].args = build_pagination_args(pagination, submenu)

    return render_template(template, **kwargs)
