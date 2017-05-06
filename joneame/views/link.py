from datetime import datetime, timedelta

from flask import redirect, request
from flask_babel import gettext as _

from joneame import app
from joneame.database import db
from joneame.views.base import paginate, render_page
from joneame.views.sidebox import (sidebox_categories, sidebox_top_links,
                                   sidebox_last_comments, sidebox_top_queued)
from joneame.views.menus import Menu, MenuButton
from joneame.models import Category, Comment, ClickCounter, Link, User
from joneame.utils import arg_to_timedelta


@app.route('/historia/<link_uri>', endpoint='Link:get')
def get_link(link_uri):
    link = (
        Link.query
        .options(db.joinedload(Link.clickcounter))
        .filter(Link.link_uri == link_uri)
        .first_or_404()
    )  # TODO revisar fecha de activacion

    comments = (
        Comment.query
        .options(db.joinedload(Comment.user).joinedload(User.avatar))
        .filter(Comment.comment_link_id == link.link_id)
    )
    pagination = paginate(comments)
    comments = pagination.items

    # count this visit
    link.visit()

    return render_page('link/linkview.html', link=link, comments=comments,
                       pagination=pagination,
                       endpoint=request.endpoint)


@app.route('/go/<int:link_id>', endpoint='Link:go')
def link_go(link_id):
    link = (
        Link.query
        .filter(Link.link_id == link_id)
        .first_or_404()
    )

    link.click()

    return redirect(link.link_url)


@app.route('/', endpoint='Link:list_home')
@app.route('/jonealas', endpoint='Link:list_queue')
@app.route('/cat/<int:category_id>', endpoint='Link:list_category')
@app.route('/las_mejores', endpoint='Link:list_top')
@app.route('/mas_visitadas', endpoint='Link:list_top_clicks')
@app.route('/aleatorias', endpoint='Link:list_random')
def get_link_list(category_id=None):
    toolbox = sidebar = title = None
    query = Link.query
    query = query.options(db.joinedload(Link.user).joinedload(User.avatar))
    query = query.options(db.joinedload(Link.category))
    query = query.options(db.joinedload(Link.clickcounter))
    query = query.options(db.joinedload(Link.visitcounter))

    ###########################################################################
    # home page. just load all published links cronologically
    ###########################################################################
    if request.endpoint == 'Link:list_home':
        query = query.filter(Link.link_status == 'published')
        query = query.order_by(Link.link_date.desc())

        sidebar = [sidebox_top_links, sidebox_categories,
                   sidebox_last_comments]

    ###########################################################################
    # queued links. load links from last month that are still in queue
    ###########################################################################
    elif request.endpoint == 'Link:list_queue':
        query = query.order_by(Link.link_sent_date.desc())

        meta = request.args.get('meta')
        if meta == 'discarded':
            my_filter = ~(Link.link_status.in_(('published', 'queued')))
            query = query.filter(my_filter)
            title = _('Discarded')
        else:
            query = query.filter(Link.link_sent_date
                                 > (datetime.utcnow() - timedelta(weeks=8)))
            query = query.filter(Link.link_status == 'queued')
            title = _('Queued')

        buttons = [
            MenuButton(text=_('all')),
            MenuButton(text=_('discarded'), icon='trash',
                       kwargs={'meta': 'discarded'}),
        ]
        toolbox = Menu(buttons=buttons, default_hint='meta')

        sidebar = [sidebox_top_queued, sidebox_categories]

    ###########################################################################
    # all published links from a category (from a sidebox)
    ###########################################################################
    elif request.endpoint == 'Link:list_category':
        category = (
            Category.query
            .filter(Category.category_id == category_id)
            .first_or_404()
        )
        query = query.filter(Link.link_status == 'published',
                             Link.link_category == category_id)
        query = query.order_by(Link.link_date.desc())
        title = _('Category: %(cat_name)s', cat_name=category.category_name)

    ###########################################################################
    # top of all time according to different time ranges
    ###########################################################################
    elif (request.endpoint == 'Link:list_top' or
          request.endpoint == 'Link:list_top_clicks'):
        query = query.filter(Link.link_status.in_(('published', 'queued')))
        if request.endpoint == 'Link:list_top':
            query = query.order_by((Link.link_votes +
                                    Link.link_anonymous).desc())
            title = _('Top links')
        elif request.endpoint == 'Link:list_top_clicks':
            query = query.join(Link.clickcounter)
            query = query.order_by(ClickCounter.clickcounter_counter.desc())
            title = _('Most clicked')

        buttons = [
            MenuButton(text=_('one day'), kwargs={'range': '24h'}),
            MenuButton(text=_('two days'), kwargs={'range': '48h'}),
            MenuButton(text=_('one week'), kwargs={'range': '1w'}),
            MenuButton(text=_('one month'), kwargs={'range': '1m'}),
            MenuButton(text=_('one year'), kwargs={'range': '1y'}),
            MenuButton(text=_('the beginning of time'),
                       kwargs={'range': 'all'}, default=True),
        ]
        toolbox = Menu(buttons=buttons, default_hint='range')

        # apply range
        td = arg_to_timedelta(request.args.get('range'))
        if td:
            query = query.filter((Link.link_date > datetime.now() - td))

    ###########################################################################
    # published and queued links, randomised
    ###########################################################################
    elif request.endpoint == 'Link:list_random':
        query = query.filter(Link.link_status.in_(('published', 'queued')))
        query = query.order_by(db.func.rand())
        title = _('Random links')

    # paginate them...
    pagination = paginate(query)
    links = pagination.items

    buttons = [
        MenuButton(endpoint='Link:list_home', text=_('home'),),
        MenuButton(endpoint='Link:list_top', text=_('top links'),
                   kwargs={'range': '24h'}),
        MenuButton(endpoint='Link:list_top_clicks', text=_('most clicked'),
                   kwargs={'range': '24h'}),
        MenuButton(endpoint='Link:list_random', text=_('random')),
        MenuButton(endpoint='Link:list_queue', text=_('queued links')),
    ]
    submenu = Menu(buttons=buttons)

    return render_page('link/linklist.html', sidebar=sidebar, links=links,
                       pagination=pagination, endpoint=request.endpoint,
                       category_id=category_id, submenu=submenu,
                       toolbox=toolbox, title=title)
