from flask import redirect, request, url_for
from flask_login import login_required

from joneame import app
from joneame.views.forms import PostForm
from joneame.models import Post


@login_required
@app.route('/ajax/new_post', endpoint='Ajax:new_post', methods={'POST'})
def new_post():
    form = PostForm(request.form)
    if form.validate_on_submit():
        Post.create(form)

    return redirect(url_for('Post:list'))
