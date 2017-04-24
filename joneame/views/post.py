from flask import abort, request, redirect, url_for
from flask_babel import gettext as _

from joneame import app
from joneame.config import _cfgi
from joneame.models import Post, User
from joneame.views.base import render_page
from joneame.views.menus import Menu, MenuButton
from joneame.utils import flatten


@app.route('/posts/<user_login>/<int:post_id>', endpoint='Post:get')
def get_post(user_login, post_id):
    post = (
        Post.query
        .filter(Post.post_id == post_id)
        .first_or_404()
    )

    if user_login != post.post_public_user:
        return redirect(url_for('Post:get', user_login=post.post_public_user,
                                post_id=post_id))

    return render_page('post/postview.html', post=post)


@app.route('/posts/', endpoint='Post:list')
@app.route('/posts/<user_login>', endpoint='Post:list_user')
def get_post_list(user_login=None):
    posts = (
        Post.query
        .filter(Post.post_parent == 0)
        .order_by(Post.post_date.desc())
    )
    if user_login:
        user = (
            User.query
            .filter(User.user_login == user_login)
            .first_or_404()
        )
        posts = posts.filter(Post.post_user_id == user.user_id)

    page = request.args.get('page', 1, type=int)
    pagination = posts.paginate(page, _cfgi('misc', 'page_size'))
    posts = pagination.items

    parent_ids = [post.post_id for post in posts]
    children = (
        Post.query
        .filter(Post.post_parent.in_(parent_ids))
        .all()
    )
    children = flatten(children, 'post_parent')

    if not posts:
        abort(404)

    buttons = [
        MenuButton(endpoint='Quote:random_redir', text=_('new post'),
                   icon='plus-square'),
    ]
    toolbox = Menu(buttons=buttons)

    return render_page('post/postlist.html', posts=posts, children=children,
                       pagination=pagination, user_login=user_login,
                       toolbox=toolbox)
