from flask_babel import gettext as _
from flask_wtf import FlaskForm
from wtforms import (TextAreaField, TextField, SubmitField, PasswordField)
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    login = TextField(_('User:'), [InputRequired(), Length(max=32)])
    password = PasswordField(_('Password:'), [InputRequired()])
    submit = SubmitField('Log in')


class CommentForm(FlaskForm):
    text = TextAreaField(_('Text:'), [InputRequired(), Length(max=5000)])
    submit = SubmitField('Submit')


class PostForm(CommentForm):
    pass
