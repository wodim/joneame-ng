from flask_babel import gettext as _
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    login = TextField(_('User:'), [InputRequired(), Length(max=32)])
    password = PasswordField(_('Password:'))
    submit = SubmitField('Log in')
