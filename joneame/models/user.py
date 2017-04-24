import base64

from flask import url_for

from joneame.config import _cfg
from joneame.database import db
from joneame.models.comment import CommentModel
from joneame.models.link import LinkModel
from joneame.models.post import PostModel


class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(32))
    user_level = db.Column(db.Enum('disabled', 'devel', 'normal', 'special',
                                   'admin', 'god'))
    user_avatar = db.Column(db.Integer)
    user_modification = db.Column(db.DateTime)
    user_date = db.Column(db.DateTime)
    user_validated_date = db.Column(db.DateTime)
    user_ip = db.Column(db.String(32))
    user_pass = db.Column(db.String(64))
    user_email = db.Column(db.String(64))
    user_names = db.Column(db.String(60))
    user_estado = db.Column(db.String(60))
    user_login_register = db.Column(db.String(32))
    user_email_register = db.Column(db.String(64))
    user_karma = db.Column(db.Integer)
    user_url = db.Column(db.String(128))
    user_thumb = db.Column(db.Boolean)

    avatar = db.relationship('AvatarModel', backref='user', uselist=False)

    links = db.relationship('LinkModel', backref='user', lazy='dynamic')
    comments = db.relationship('CommentModel', backref='user', lazy='dynamic')
    posts = db.relationship('PostModel', backref='user', lazy='dynamic')
    quotes = db.relationship('QuoteModel', backref='user', lazy='dynamic')

    @property
    def avatar_url(self, size=80):
        if self.avatar:
            # TODO
            return ('data:image/jpeg;base64,' +
                    base64.b64encode(self.avatar.avatar_image).decode('utf-8'))
        else:
            return url_for('static', filename=_cfg('misc', 'no_avatar_image'))

    @property
    def links_published_count(self):
        query = LinkModel.query
        query = query.filter(LinkModel.link_author == self.user_id)
        query = query.filter(LinkModel.link_status == 'published')
        return query.count()

    # next functions are necessary to hide admin contents from counts
    @property
    def comments_count(self):
        query = CommentModel.query
        query = query.filter(CommentModel.comment_user_id == self.user_id)
        query = query.filter(CommentModel.comment_type == 'normal')
        return query.count()

    @property
    def posts_count(self):
        query = PostModel.query
        query = query.filter(PostModel.post_user_id == self.user_id)
        query = query.filter(PostModel.post_type == 'normal')
        return query.count()

    def __repr__(self):
        return '<User %r, nick %r>' % (self.user_id, self.user_login)


class AvatarModel(db.Model):
    __tablename__ = 'avatars'

    avatar_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                          primary_key=True)
    avatar_image = db.Column(db.LargeBinary)
    avatar_modified = db.Column(db.DateTime)

    def __repr__(self):
        return '<Avatar %r, modified %r>' % (self.avatar_id,
                                             self.avatar_modified)
    """user = db.relationship('UserModel', uselist=False,
                            back_populates='avatar')"""
