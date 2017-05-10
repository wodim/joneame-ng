import base64
import hashlib

from flask import url_for

from joneame.database import db
from joneame.mixins import MyUserMixin


class User(MyUserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    login = db.Column('user_login', db.String(32))
    level = db.Column('user_level',
                      db.Enum('disabled', 'devel', 'normal', 'special',
                              'admin', 'god'))
    avatar = db.Column('user_avatar', db.Integer)
    modification = db.Column('user_modification', db.DateTime)
    date = db.Column('user_date', db.DateTime)
    validated_date = db.Column('user_validated_date', db.DateTime)
    ip = db.Column('user_ip', db.String(32))
    password = db.Column('user_pass', db.String(64))
    email = db.Column('user_email', db.String(64))
    names = db.Column('user_names', db.String(60))
    estado = db.Column('user_estado', db.String(60))
    login_register = db.Column('user_login_register', db.String(32))
    email_register = db.Column('user_email_register', db.String(64))
    karma = db.Column('user_karma', db.Integer)
    url = db.Column('user_url', db.String(128))
    thumb = db.Column('user_thumb', db.Boolean)

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
                    base64.b64encode(self.avatar.image).decode('utf-8'))
        return url_for('static', filename='images/no-avatar.png')

    @property
    def votes_count(self):
        # this is useless, because the votes table is purged regularly.
        # it's the way it's done currently even in menéame, so...
        return self.votes.count()

    @property
    def links_published_count(self):
        from joneame.models import Link

        query = Link.query
        query = query.filter(Link.author == self.id)
        query = query.filter(Link.status == 'published')
        return query.count()

    # next functions are necessary to hide admin contents from counts
    @property
    def comments_count(self):
        from joneame.models.comment import Comment

        query = Comment.query
        query = query.filter(Comment.id == self.id)
        query = query.filter(Comment.type == 'normal')
        return query.count()

    @property
    def posts_count(self):
        from joneame.models.post import Post

        query = Post.query
        query = query.filter(Post.id == self.id)
        query = query.filter(Post.type == 'normal')
        return query.count()

    def check_password(self, password):
        h = hashlib.new('md5')
        h.update(password.encode('utf8'))
        password = h.hexdigest()
        return self.password == password

    def get_id(self):
        return self.id

    @property
    def is_admin(self):
        return self.level in ('god', 'admin')

    def __repr__(self):
        return '<User %r, nick %r>' % (self.id, self.login)


class Avatar(db.Model):
    __tablename__ = 'avatars'

    id = db.Column('avatar_id', db.Integer, db.ForeignKey('users.user_id'),
                   primary_key=True)
    image = db.Column('avatar_image', db.LargeBinary)
    modified = db.Column('avatar_modified', db.DateTime)

    user = db.relationship('User', back_populates='avatar', uselist=False,
                           lazy='select')

    def __repr__(self):
        return '<Avatar %r, modified %r>' % (self.id,
                                             self.modified)
