from hashlib import md5

from ..database import db

class UserModel(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_login = db.Column(db.String(32))
    user_level = db.Column(db.Enum(['disabled', 'devel', 'normal', 'special', 'admin', 'god']))
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

    links = db.relationship('LinkModel', backref='user', lazy="dynamic")
    comments = db.relationship('CommentModel', backref='user', lazy="dynamic")
    posts = db.relationship('PostModel', backref='user', lazy="dynamic")
    quotes = db.relationship('QuoteModel', backref='user', lazy="dynamic")

    def avatar_hash(self):
        m = md5(bytearray(self.user_email.lower(), encoding="utf8"))
        return m.hexdigest()

    def get_avatar_url(self, size=80):
        tpl = "http://www.gravatar.com/avatar/{hash}?s={size}&d=retro"
        return tpl.format(hash=self.avatar_hash, size=size)

    def __repr__(self):
        return '<User %r, nick %r>' % (self.user_id, self.user_login)