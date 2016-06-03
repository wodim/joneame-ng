from flask import abort, request, render_template
from flask_classy import FlaskView, route

from ..config import _cfgi
from ..models import CommentModel, LinkModel, QuoteModel, UserModel

class UserView(FlaskView):
    route_base = '/'

    @route('/mafioso/<user_login>')
    def get(self, user_login):
        user = UserModel.query.filter(UserModel.user_login == user_login).first_or_404() # revisar fecha de activacion

        return render_template('user/user.html', user=user)

    @route('/mafioso/<user_login>/cortos')
    def get_quotes(self, user_login):
        user = UserModel.query.filter(UserModel.user_login == user_login).first_or_404() # revisar fecha de activacion

        query = QuoteModel.query
        query = query.filter(QuoteModel.quote_author == user.user_id)
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        quotes = pagination.items

        if not quotes:
            abort(404)

        return render_template('user/quotelist.html', user_login=user.user_login,
                                                      quotes=quotes,
                                                      pagination=pagination,
                                                      endpoint=request.endpoint)

    @route('/mafioso/<user_login>/historias')
    def get_links(self, user_login):
        user = UserModel.query.filter(UserModel.user_login == user_login).first_or_404() # revisar fecha de activacion

        query = LinkModel.query
        query = query.filter(LinkModel.link_author == user.user_id)
        query = query.order_by(LinkModel.link_date.desc())
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        links = pagination.items

        if not links:
            abort(404)

        return render_template('user/linklist.html', user_login=user.user_login,
                                                     links=links,
                                                     pagination=pagination,
                                                     endpoint=request.endpoint)

    @route('/mafioso/<user_login>/comentarios')
    def get_comments(self, user_login):
        user = UserModel.query.filter(UserModel.user_login == user_login).first_or_404() # revisar fecha de activacion

        query = CommentModel.query
        query = query.filter(CommentModel.comment_user_id == user.user_id)
        query = query.order_by(CommentModel.comment_date.desc())
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        comments = pagination.items

        if not comments:
            abort(404)

        return render_template('user/commentlist.html', user_login=user.user_login,
                                                        comments=comments,
                                                        pagination=pagination,
                                                        endpoint=request.endpoint)
