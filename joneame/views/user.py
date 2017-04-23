from flask import abort, request

from joneame import app
from joneame.config import _cfgi
from joneame.models import CommentModel, LinkModel, QuoteModel, UserModel
from joneame.views.base import render_page


@app.route('/mafioso/<user_login>', endpoint='User:get')
def get_user(user_login):
    user = (
        UserModel.query
        .filter(UserModel.user_login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    return render_page('user/user.html', user=user)


@app.route('/mafioso/<user_login>/cortos')
def get_user_quotes(user_login):
    user = (
        UserModel.query
        .filter(UserModel.user_login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    query = QuoteModel.query
    query = query.filter(QuoteModel.quote_author == user.user_id)
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, _cfgi('misc', 'page_size'))
    quotes = pagination.items

    if not quotes:
        abort(404)

    return render_page('user/quotelist.html', user_login=user.user_login,
                       quotes=quotes, pagination=pagination,
                       endpoint=request.endpoint)


@app.route('/mafioso/<user_login>/historias')
def get_user_links(user_login):
    user = (
        UserModel.query
        .filter(UserModel.user_login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    query = LinkModel.query
    query = query.filter(LinkModel.link_author == user.user_id)
    query = query.order_by(LinkModel.link_date.desc())
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, _cfgi('misc', 'page_size'))
    links = pagination.items

    if not links:
        abort(404)

    return render_page('user/linklist.html', user_login=user.user_login,
                       links=links, pagination=pagination,
                       endpoint=request.endpoint)


@app.route('/mafioso/<user_login>/comentarios')
def get_user_comments(user_login):
    user = (
        UserModel.query
        .filter(UserModel.user_login == user_login)
        .first_or_404()
    )  # revisar fecha de activacion

    query = CommentModel.query
    query = query.filter(CommentModel.comment_user_id == user.user_id)
    query = query.order_by(CommentModel.comment_date.desc())
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, _cfgi('misc', 'page_size'))
    comments = pagination.items

    if not comments:
        abort(404)

    return render_page('user/commentlist.html', user_login=user.user_login,
                       comments=comments, pagination=pagination,
                       endpoint=request.endpoint)
