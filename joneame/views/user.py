from flask import request
from flask_babel import gettext as _

from joneame import app
from joneame.config import _cfgi
from joneame.controllers import UserLinkList
from joneame.models import Comment, Post, Quote, User
from joneame.views.base import paginate, render_page
from joneame.views.menus import Menu, MenuButton


@app.route('/mafioso/<user_login>', endpoint='User:get')
@app.route('/mafioso/<user_login>/cortos', endpoint='User:get_quotes')
@app.route('/mafioso/<user_login>/historias', endpoint='User:get_links')
@app.route('/mafioso/<user_login>/comentarios', endpoint='User:get_comments')
def get_user(user_login):
    user = (
        User.query
        .filter(User.login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    page_size = _cfgi('misc', 'page_size')

    if request.endpoint == 'User:get':
        template = 'user/user.html'
        query = (
            Post.query
            .filter(Post.user_id == user.id)
            .order_by(Post.id.desc())
        )
        page_size = 1
    elif request.endpoint == 'User:get_quotes':
        template = 'user/quotelist.html'
        query = Quote.query
        query = query.filter(Quote.author == user.id)
        query = query.order_by(Quote.id.asc())
        page_size *= 2.5
    elif request.endpoint == 'User:get_links':
        template = 'user/linklist.html'
        link_list = UserLinkList(user_id=user.id)
        link_list.fetch()
    elif request.endpoint == 'User:get_comments':
        template = 'user/commentlist.html'
        query = Comment.query
        query = query.filter(Comment.user_id == user.id)
        query = query.order_by(Comment.date.desc())

    if request.endpoint == 'User:get_links':
        pagination = link_list.pagination
        items = link_list.items
    else:
        pagination = paginate(query, page_size)
        items = pagination.items

    buttons = [
        MenuButton(endpoint='User:get', text='usuario',
                   kwargs=dict(user_login=user_login)),
        MenuButton(endpoint='User:get_quotes', text=_('quotes'),
                   kwargs=dict(user_login=user_login)),
        MenuButton(endpoint='User:get_links', text=_('links'),
                   kwargs=dict(user_login=user_login)),
        MenuButton(endpoint='User:get_comments', text=_('comments'),
                   kwargs=dict(user_login=user_login)),
        MenuButton(endpoint='Post:list_user', text=_('posts'),
                   kwargs=dict(user_login=user_login)),
    ]
    submenu = Menu(buttons=buttons)

    return render_page(template, user=user, items=items, submenu=submenu,
                       pagination=pagination, user_login=user_login)
