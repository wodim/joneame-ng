from datetime import datetime

from flask import abort, redirect, request, url_for
from flask_babel import gettext as _
from flask_login import current_user

from joneame import app
from joneame.database import db
from joneame.models import Post, User
from joneame.views.base import paginate, render_page
from joneame.views.forms import PostForm
from joneame.views.menus import Menu, MenuButton
from joneame.utils import arg_to_timedelta, flatten


post_buttons = [
    MenuButton(endpoint='Post:list', text=_('all'),),
    MenuButton(endpoint='Post:list_top', text=_('best'),
               kwargs={'range': '24h'}),
]


@app.route('/notitas/<user_login>/<int:post_id>', endpoint='Post:get')
def get_post(user_login, post_id):
    thread = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
        .filter((Post.id == post_id) | (Post.parent == post_id))
        .all()
    )

    if not thread:
        abort(404)

    if user_login != thread[0].public_user:
        return redirect(url_for('Post:get',
                                user_login=thread[0].public_user,
                                post_id=post_id))

    parents = thread[:1]
    children = {post_id: [post for post in thread if post.parent]}

    submenu = Menu(buttons=post_buttons)

    return render_page('post/postlist.html', posts=parents, children=children,
                       submenu=submenu)


@app.route('/notitas/', endpoint='Post:list')
@app.route('/notitas/<user_login>', endpoint='Post:list_user')
def get_post_list(user_login=None):
    posts = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
        .filter(Post.parent == 0)
        .order_by(Post.date.desc())
        .order_by(Post.last_answer.desc())
    )
    if user_login:
        user = (
            User.query
            .filter(User.login == user_login)
            .first_or_404()
        )
        posts = posts.filter(Post.user_id == user.id,
                             Post.type.in_(('normal', 'encuesta')))

    pagination = paginate(posts)
    posts = pagination.items

    parent_ids = [post.id for post in posts]
    children = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
        .filter(Post.parent.in_(parent_ids))
        .all()
    )
    children = flatten(children, 'parent')

    if not posts:
        abort(404)

    buttons = [
        MenuButton(endpoint='Post:list', text=_('new post'),
                   icon='plus-square'),
    ]
    submenu = Menu(buttons=post_buttons)
    toolbox = Menu(buttons=buttons)

    form = PostForm() if current_user.is_authenticated else None

    return render_page('post/postlist.html', posts=posts, children=children,
                       pagination=pagination, user_login=user_login,
                       submenu=submenu, toolbox=toolbox, form=form)


@app.route('/notitas/_mejores', endpoint='Post:list_top')
def get_post_top_list():
    posts = (
        Post.query
        .options(db.joinedload(Post.user).joinedload(User.avatar))
        .filter(Post.parent == 0)
        .order_by(Post.karma.desc())
    )

    td = arg_to_timedelta(request.args.get('range'))
    if td:
        posts = posts.filter((Post.date > datetime.now() - td))

    pagination = paginate(posts)
    posts = pagination.items

    buttons = [
            MenuButton(text=_('one day'), kwargs={'range': '24h'}),
            MenuButton(text=_('two days'), kwargs={'range': '48h'}),
            MenuButton(text=_('one week'), kwargs={'range': '1w'}),
            MenuButton(text=_('one month'), kwargs={'range': '1m'}),
            MenuButton(text=_('one year'), kwargs={'range': '1y'}),
            MenuButton(text=_('the beginning of time'),
                       kwargs={'range': 'all'}, default=True),
    ]

    submenu = Menu(buttons=post_buttons)
    toolbox = Menu(buttons=buttons, default_hint='range')

    return render_page('post/postlist.html', posts=posts,
                       pagination=pagination, submenu=submenu, toolbox=toolbox)
