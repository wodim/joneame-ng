from flask import abort, request
from flask_babel import gettext as _

from joneame import app
from joneame.database import db
from joneame.views.base import render_page
from joneame.views.sidebox import (sidebox_categories, sidebox_top_links,
                                   sidebox_last_comments, sidebox_top_queued)
from joneame.views.menus import Menu, MenuButton
from joneame.models import LinkModel, CommentModel, CategoryModel
from joneame.config import _cfgi

from datetime import datetime, timedelta


@app.route('/historia/<link_uri>', endpoint='Link:get')
def get_link(link_uri):
    link = (
        LinkModel.query
        .filter(LinkModel.link_uri == link_uri)
        .first_or_404()
    )  # TODO revisar fecha de activacion

    comments = (
        CommentModel.query
        .filter(CommentModel.comment_link_id == link.link_id)
    )
    page = request.args.get('page', 1, type=int)
    pagination = comments.paginate(page, _cfgi('misc', 'page_size'))
    comments = pagination.items

    return render_page('link/linkview.html', link=link, comments=comments,
                       pagination=pagination,
                       endpoint=request.endpoint)


@app.route('/', endpoint='Link:list_home')
@app.route('/queue', endpoint='Link:list_queue')
@app.route('/category/<int:category_id>', endpoint='Link:list_category')
@app.route('/top', endpoint='Link:list_top')
def get_link_list(category_id=None):
    toolbox = sidebar = None
    query = LinkModel.query
    if request.endpoint == 'Link:list_home':
        query = query.filter(LinkModel.link_status == 'published')
        query = query.order_by(LinkModel.link_sent_date.desc())

        sidebar = [sidebox_categories, sidebox_top_links,
                   sidebox_last_comments]
    elif request.endpoint == 'Link:list_queue':
        query = query.filter(LinkModel.link_status == 'queued',
                             LinkModel.link_sent_date
                             > (datetime.utcnow() - timedelta(weeks=4)))
        query = query.order_by(LinkModel.link_sent_date.desc())

        sidebar = [sidebox_top_queued]
    elif request.endpoint == 'Link:list_category':
        query = query.filter(LinkModel.link_status == 'published',
                             LinkModel.link_category == category_id)
        query = query.order_by(LinkModel.link_sent_date.desc())
    elif request.endpoint == 'Link:list_top':
        query = query.filter(LinkModel.link_status == 'published')
        query = query.order_by((LinkModel.link_votes +
                                LinkModel.link_anonymous).desc())
        buttons = [
            MenuButton(endpoint='Link:list_top', text=_('one day'),
                       kwargs={'range': '24h'}),
            MenuButton(endpoint='Link:list_top', text=_('two days'),
                       kwargs={'range': '48h'}),
            MenuButton(endpoint='Link:list_top', text=_('one week'),
                       kwargs={'range': '1w'}),
            MenuButton(endpoint='Link:list_top', text=_('one month'),
                       kwargs={'range': '1m'}),
            MenuButton(endpoint='Link:list_top', text=_('one year'),
                       kwargs={'range': '1y'}),
            MenuButton(endpoint='Link:list_top',
                       text=_('the beginning of time'),
                       kwargs={'range': 'all'}),
        ]
        toolbox = Menu(buttons=buttons, required_key='range')

    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, _cfgi('misc', 'page_size'))
    links = pagination.items

    if not links:
        abort(404)

    buttons = [
        MenuButton(endpoint='Link:list_home', text=_('home'),),
        MenuButton(endpoint='Link:list_top', text=_('top links'),
                   kwargs={'range': '24h'}),
        MenuButton(endpoint='Link:list_queue', text=_('queued links')),
    ]
    submenu = Menu(buttons=buttons, auto_endpoint=True)

    return render_page('link/linklist.html', sidebar=sidebar, links=links,
                       pagination=pagination, endpoint=request.endpoint,
                       category_id=category_id, submenu=submenu,
                       toolbox=toolbox)
