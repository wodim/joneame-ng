from flask_babel import gettext as _
from flask_wtf import FlaskForm
from wtforms import (TextAreaField, TextField, SubmitField, PasswordField)
from wtforms.validators import InputRequired, Length


custom_ir = InputRequired(message=_('This field cannot be empty.'))


class LoginForm(FlaskForm):
    login = TextField(_('User:'), [custom_ir, Length(max=32)])
    password = PasswordField(_('Password:'), [custom_ir])
    submit = SubmitField('Log in')


class CommentForm(FlaskForm):
    text = TextAreaField(_('Text:'), [custom_ir, Length(max=5000)])
    submit = SubmitField('Submit')


class PostForm(CommentForm):
    pass
