from flask import abort, flash, redirect, request, url_for
from flask_babel import gettext as _
from flask_login import login_required, login_user, logout_user

from joneame import app
from joneame.models import User
from joneame.views.base import render_page
from joneame.views.forms import LoginForm
from joneame.utils import is_safe_url


@app.route('/login', endpoint='Session:login_form', methods=('GET', 'POST'))
def login_form():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = (
            User.query
            .filter((User.user_login == form.login.data) |
                    (User.user_email == form.login.data))
            .filter(User.user_level != 'disabled')  # TODO: more levels?
            .first()
        )

        if user and user.check_password(form.password.data):
            login_user(user)
            flash(_('Welcome back!'))

            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or url_for('Link:list_home'))
        else:
            flash(_('Invalid user/email or password'))
    return render_page('login.html', form=form)


# TODO: CSRF
@app.route('/logout', endpoint='Session:logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.')
    return redirect(url_for('Link:list_home'))
