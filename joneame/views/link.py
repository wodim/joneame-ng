from flask import abort, redirect, request

from joneame import app
from joneame.controllers import (CategoryLinkList, HomeLinkList,
                                 QueuedLinkList, TopVotesLinkList,
                                 TopClicksLinkList, RandomLinkList,
                                 SingleLink)
from joneame.database import db
from joneame.views.base import paginate, render_page
from joneame.models import Comment, Link, User


@app.route('/historia/<link_uri>', endpoint='Link:get')
def get_link(link_uri):
    link_list = SingleLink(link_uri=link_uri)
    link_list.fetch()

    if link_list.count < 1:
        abort(404)

    link = link_list.items[0]

    comments = (
        Comment.query
        .options(db.joinedload(Comment.user).joinedload(User.avatar))
        .filter(Comment.link_id == link.id)
    )
    pagination = paginate(comments)
    comments = pagination.items

    # count this visit
    # TODO implement l_v stuff
    link.visit()

    return render_page('link/linksingle.html', link=link, comments=comments,
                       pagination=pagination)


@app.route('/go/<int:link_id>', endpoint='Link:go')
def link_go(link_id):
    link = (
        Link.query
        .filter(Link.id == link_id)
        .first_or_404()
    )

    link.click()

    return redirect(link.url)


@app.route('/', endpoint='Link:list_home')
@app.route('/jonealas', endpoint='Link:list_queue')
@app.route('/cat/<int:category_id>', endpoint='Link:list_category')
@app.route('/las_mejores', endpoint='Link:list_top')
@app.route('/mas_visitadas', endpoint='Link:list_top_clicks')
@app.route('/aleatorias', endpoint='Link:list_random')
def link_list(category_id=None):
    if request.endpoint == 'Link:list_home':
        link_list = HomeLinkList()
    elif request.endpoint == 'Link:list_queue':
        meta = request.args.get('meta')
        link_list = QueuedLinkList(meta)
    elif request.endpoint == 'Link:list_category':
        try:
            link_list = CategoryLinkList(category_id)
        except KeyError:
            abort(404)
    elif request.endpoint == 'Link:list_top':
        range = request.args.get('range')
        link_list = TopVotesLinkList(range)
    elif request.endpoint == 'Link:list_top_clicks':
        range = request.args.get('range')
        link_list = TopClicksLinkList(range)
    elif request.endpoint == 'Link:list_random':
        link_list = RandomLinkList()

    link_list.page = request.args.get('page', 1, type=int)
    link_list.fetch()

    return render_page('link/linklist.html', sidebar=link_list.sidebar,
                       links=link_list.items, pagination=link_list.pagination,
                       submenu=link_list.submenu, title=link_list.title,
                       toolbox=link_list.toolbox)
