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
    
    links = db.relationship('LinkModel', backref='user')
    comments = db.relationship('CommentModel', backref='user')
    posts = db.relationship('PostModel', backref='user')

    def __repr__(self):
        return '<User %r, nick %r>' % (self.user_id, self.user_login)