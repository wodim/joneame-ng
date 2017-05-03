from flask import abort, redirect, url_for
from flask_babel import gettext as _

from joneame import app
from joneame.database import db
from joneame.models import Post, User
from joneame.views.base import paginate, render_page
from joneame.views.menus import Menu, MenuButton
from joneame.utils import flatten


@app.route('/notitas/<user_login>/<int:post_id>', endpoint='Post:get')
def get_post(user_login, post_id):
    thread = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
        .filter((Post.post_id == post_id) | (Post.post_parent == post_id))
        .all()
    )

    if user_login != thread[0].post_public_user:
        return redirect(url_for('Post:get',
                                user_login=thread[0].post_public_user,
                                post_id=post_id))

    parents = thread[:1]
    children = {post_id: [post for post in thread if post.post_parent]}

    return render_page('post/postlist.html', posts=parents, children=children)


@app.route('/notitas/', endpoint='Post:list')
@app.route('/notitas/<user_login>', endpoint='Post:list_user')
def get_post_list(user_login=None):
    posts = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
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
        posts = posts.filter(Post.post_type != 'admin')

    pagination = paginate(posts)
    posts = pagination.items

    parent_ids = [post.post_id for post in posts]
    children = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
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
