from flask import abort, render_template, request, redirect
from flask.ext.classy import FlaskView, route

from ..models import PostModel, UserModel
from ..config import _cfgi

class PostView(FlaskView):
    route_base = '/'

    @route('/posts/<user_login>/<int:post_id>')
    def get(self, user_login, post_id):
        post = PostView.query.filter(PostModel.post_id == post_id).first_or_404()

        if post.user.user_login != user_login:
            return redirect(url_for('PostView', user_login=post.user.user_login, post_id=post_id))

        return render_template('postview.html', post=post)

class PostListView(FlaskView):
    route_base = '/'

    @route('/posts/')
    def get(self, page=1):
        query = PostModel.query.filter(PostModel.post_parent == 0).order_by('post_date desc')

        try:
            page = int(request.args['page'])
        except:
            page = 1

        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        posts = pagination.items

        if posts == None:
            abort(404)

        return render_template('postlist.html', posts=posts, pagination=pagination, endpoint=request.endpoint)