from datetime import datetime, timedelta

from flask import redirect, request
from flask_babel import gettext as _

from joneame import app
from joneame.database import db
from joneame.views.base import render_page
from joneame.views.sidebox import (sidebox_categories, sidebox_top_links,
                                   sidebox_last_comments, sidebox_top_queued)
from joneame.views.menus import Menu, MenuButton
from joneame.models import Link, Comment, User
from joneame.config import _cfgi


@app.route('/historia/<link_uri>', endpoint='Link:get')
def get_link(link_uri):
    link = (
        Link.query
        .filter(Link.link_uri == link_uri)
        .first_or_404()
    )  # TODO revisar fecha de activacion

    comments = (
        Comment.query
        .filter(Comment.comment_link_id == link.link_id)
    )
    page = request.args.get('page', 1, type=int)
    pagination = comments.paginate(page, _cfgi('misc', 'page_size'))
    comments = pagination.items

    return render_page('link/linkview.html', link=link, comments=comments,
                       pagination=pagination,
                       endpoint=request.endpoint)


@app.route('/go/<int:link_id>', endpoint='Link:go')
def link_go(link_id):
    # TODO track clicks
    link = (
        Link.query
        .filter(Link.link_id == link_id)
        .first_or_404()
    )  # TODO revisar fecha de activacion

    return redirect(link.link_url)


@app.route('/', endpoint='Link:list_home')
@app.route('/jonealas', endpoint='Link:list_queue')
@app.route('/cat/<int:category_id>', endpoint='Link:list_category')
@app.route('/las_mejores', endpoint='Link:list_top')
def get_link_list(category_id=None):
    toolbox = sidebar = None
    query = Link.query
    query = query.options(db.joinedload(Link.user).joinedload(User.avatar))
    query = query.options(db.joinedload(Link.category))

    # home page. just load all published links cronologically
    if request.endpoint == 'Link:list_home':
        query = query.filter(Link.link_status == 'published')
        query = query.order_by(Link.link_date.desc())

        sidebar = [sidebox_categories, sidebox_top_links,
                   sidebox_last_comments]

    # queued links. load links from last month that are still in queue
    elif request.endpoint == 'Link:list_queue':
        query = query.filter(Link.link_status == 'queued',
                             Link.link_sent_date
                             > (datetime.utcnow() - timedelta(weeks=4)))
        query = query.order_by(Link.link_sent_date.desc())

        buttons = [
            MenuButton(endpoint='Link:list_queue', text=_('all')),
            MenuButton(endpoint='Link:list_queue', text=_('discarded'),
                       icon='trash', kwargs={'meta': 'discarded'}),
        ]
        toolbox = Menu(buttons=buttons, required_key='meta')

        sidebar = [sidebox_top_queued]

    # all published links from a category (from a sidebox)
    elif request.endpoint == 'Link:list_category':
        query = query.filter(Link.link_status == 'published',
                             Link.link_category == category_id)
        query = query.order_by(Link.link_date.desc())

    # top of all time according to different time ranges
    elif request.endpoint == 'Link:list_top':
        query = query.filter(Link.link_status == 'published')
        query = query.order_by((Link.link_votes +
                                Link.link_anonymous).desc())
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

        v_to_r = {'24h': timedelta(hours=24),
                  '48h': timedelta(hours=48),
                  '1w':  timedelta(weeks=1),
                  '1m':  timedelta(weeks=4),
                  '1y':  timedelta(days=365)}

        timerange = request.args.get('range')
        if timerange and timerange in v_to_r:
            query = query.filter((Link.link_date >
                                  datetime.now() - v_to_r[timerange]))

    # paginate them...
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, _cfgi('misc', 'page_size'))
    links = pagination.items

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
