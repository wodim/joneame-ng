from flask_login import LoginManager

from joneame import app
from joneame.database import db
from joneame.mixins import MyAnonymousUserMixin
from joneame.models import User


# initialise the login manager
login_manager = LoginManager(app)
login_manager.anonymous_user = MyAnonymousUserMixin


@login_manager.user_loader
def load_user(id):
    query = User.query.options(db.joinedload(User.avatar))
    return query.get(int(id))
