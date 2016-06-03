from flask import abort, render_template, request, redirect, url_for
from flask_classy import FlaskView, route

from ..models import PostModel
from ..config import _cfgi

class PostView(FlaskView):
    route_base = '/'

    @route('/posts/<user_login>/<int:post_id>')
    def get(self, user_login, post_id):
        post = PostModel.query.filter(PostModel.post_id == post_id).first_or_404()

        if post.user.user_login != user_login:
            return redirect(url_for('PostView:get',
                                        user_login=post.user.user_login,
                                        post_id=post_id))

        return render_template('post/postview.html', post=post)

class PostListView(FlaskView):
    route_base = '/'

    @route('/posts/')
    def get(self, page=1):
        query = PostModel.query.filter(PostModel.post_parent == 0)
        query = query.order_by(PostModel.post_date.desc())
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        posts = pagination.items

        if not posts:
            abort(404)

        return render_template('post/postlist.html', posts=posts,
                                                     pagination=pagination,
                                                     endpoint=request.endpoint)