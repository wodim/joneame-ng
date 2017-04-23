from flask import abort, request, redirect, url_for

from joneame import app
from joneame.config import _cfgi
from joneame.models import PostModel
from joneame.views.base import render_page


@app.route('/posts/<user_login>/<int:post_id>')
def get_post(user_login, post_id):
    post = (
        PostModel.query
        .filter(PostModel.post_id == post_id)
        .first_or_404()
    )

    if post.user.user_login != user_login:
        return redirect(url_for('Post:get', user_login=post.user.user_login,
                                post_id=post_id))

    return render_page('post/postview.html', post=post)


@app.route('/posts/', endpoint='Post:list')
def get_post_list(page=1):
    posts = (
        PostModel.query
        .filter(PostModel.post_parent == 0)
        .order_by(PostModel.post_date.desc())
    )

    page = request.args.get('page', 1, type=int)
    pagination = posts.paginate(page, _cfgi('misc', 'page_size'))
    posts = pagination.items

    if not posts:
        abort(404)

    return render_page('post/postlist.html', posts=posts,
                       pagination=pagination, endpoint=request.endpoint)
