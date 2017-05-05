import base64
import hashlib

from flask import url_for
from flask_login import UserMixin

from joneame import login_manager
from joneame.database import db
from joneame.models.comment import Comment
from joneame.models.link import Link
from joneame.models.post import Post


class User(UserMixin, db.Model):
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

    avatar = db.relationship('Avatar', back_populates='user', uselist=False)
    links = db.relationship('Link', back_populates='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    posts = db.relationship('Post', back_populates='user', lazy='dynamic')
    quotes = db.relationship('Quote', backref='user', lazy='dynamic')
    votes = db.relationship('Vote', back_populates='user', lazy='dynamic')

    @property
    def avatar_url(self, size=80):
        if self.avatar:
            # TODO
            return ('data:image/jpeg;base64,' +
                    base64.b64encode(self.avatar.avatar_image).decode('utf-8'))
        return url_for('static', filename='images/no-avatar.png')

    @property
    def votes_count(self):
        # this is useless, because the votes table is purged regularly.
        # it's the way it's done currently even in menéame, so...
        return self.votes.count()

    @property
    def links_published_count(self):
        query = Link.query
        query = query.filter(Link.link_author == self.user_id)
        query = query.filter(Link.link_status == 'published')
        return query.count()

    # next functions are necessary to hide admin contents from counts
    @property
    def comments_count(self):
        query = Comment.query
        query = query.filter(Comment.comment_user_id == self.user_id)
        query = query.filter(Comment.comment_type == 'normal')
        return query.count()

    @property
    def posts_count(self):
        query = Post.query
        query = query.filter(Post.post_user_id == self.user_id)
        query = query.filter(Post.post_type == 'normal')
        return query.count()

    def check_password(self, password):
        h = hashlib.new('md5')
        h.update(password.encode('utf8'))
        password = h.hexdigest()
        return self.user_pass == password

    def get_id(self):
        return self.user_id

    def __repr__(self):
        return '<User %r, nick %r>' % (self.user_id, self.user_login)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Avatar(db.Model):
    __tablename__ = 'avatars'

    avatar_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                          primary_key=True)
    avatar_image = db.Column(db.LargeBinary)
    avatar_modified = db.Column(db.DateTime)

    user = db.relationship('User', back_populates='avatar', uselist=False,
                           lazy='select')

    def __repr__(self):
        return '<Avatar %r, modified %r>' % (self.avatar_id,
                                             self.avatar_modified)


class Vote(db.Model):
    __tablename__ = 'votes'

    vote_id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.Enum('links', 'comments', 'posts', 'cortos',
                                  'poll_comment'))
    vote_date = db.Column(db.DateTime)
    vote_link_id = db.Column(db.Integer)
    vote_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    vote_value = db.Column(db.Integer)
    vote_ip_int = db.Column(db.Integer)  # !!!
    vote_aleatorio = db.Column(db.Enum('normal', 'aleatorio'))

    user = db.relationship('User', back_populates='votes', uselist=False)

    def __repr__(self):
        return ('<Vote %r, type %r, user %r, thing %r, value %r>' %
                self.vote_id, self.vote_type, self.vote_user_id, self.link_id,
                self.value)
