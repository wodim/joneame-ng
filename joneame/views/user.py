from flask import request
from flask_babel import gettext as _

from joneame import app
from joneame.config import _cfgi
from joneame.models import CommentModel, LinkModel, QuoteModel, UserModel
from joneame.views.base import render_page
from joneame.views.menus import Menu, MenuButton


@app.route('/mafioso/<user_login>', endpoint='User:get')
@app.route('/mafioso/<user_login>/cortos', endpoint='User:get_quotes')
@app.route('/mafioso/<user_login>/historias', endpoint='User:get_links')
@app.route('/mafioso/<user_login>/comentarios', endpoint='User:get_comments')
def get_user(user_login):
    user = (
        UserModel.query
        .filter(UserModel.user_login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    if request.endpoint == 'User:get':
        template = 'user/user.html'
        items = pagination = None
    else:
        if request.endpoint == 'User:get_quotes':
            template = 'user/quotelist.html'
            query = QuoteModel.query
            query = query.filter(QuoteModel.quote_author == user.user_id)
        elif request.endpoint == 'User:get_links':
            template = 'user/linklist.html'
            query = LinkModel.query
            query = query.filter(LinkModel.link_author == user.user_id)
            query = query.order_by(LinkModel.link_date.desc())
        elif request.endpoint == 'User:get_comments':
            template = 'user/commentlist.html'
            query = CommentModel.query
            query = query.filter(CommentModel.comment_user_id == user.user_id)
            query = query.order_by(CommentModel.comment_date.desc())
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
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
    submenu = Menu(buttons=buttons, auto_endpoint=True)

    return render_page(template, user=user, items=items, submenu=submenu,
                       pagination=pagination, user_login=user_login)
