from flask import request
from flask_babel import gettext as _

from joneame import app
from joneame.config import _cfgi
from joneame.models import Comment, Link, Quote, User
from joneame.views.base import paginate, render_page
from joneame.views.menus import Menu, MenuButton


@app.route('/mafioso/<user_login>', endpoint='User:get')
@app.route('/mafioso/<user_login>/cortos', endpoint='User:get_quotes')
@app.route('/mafioso/<user_login>/historias', endpoint='User:get_links')
@app.route('/mafioso/<user_login>/comentarios', endpoint='User:get_comments')
def get_user(user_login):
    user = (
        User.query
        .filter(User.user_login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    page_size = _cfgi('misc', 'page_size')

    if request.endpoint == 'User:get':
        template = 'user/user.html'
        items = pagination = None
    else:
        if request.endpoint == 'User:get_quotes':
            template = 'user/quotelist.html'
            query = Quote.query
            query = query.filter(Quote.quote_author == user.user_id)
            query = query.order_by(Quote.quote_id.asc())
            page_size *= 2
        elif request.endpoint == 'User:get_links':
            template = 'user/linklist.html'
            query = Link.query
            query = query.filter(Link.link_author == user.user_id)
            query = query.order_by(Link.link_date.desc())
        elif request.endpoint == 'User:get_comments':
            template = 'user/commentlist.html'
            query = Comment.query
            query = query.filter(Comment.comment_user_id == user.user_id)
            query = query.order_by(Comment.comment_date.desc())
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
