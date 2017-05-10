from joneame.database import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column('post_id', db.Integer, primary_key=True)
    randkey = db.Column('post_randkey', db.Integer)
    src = db.Column('post_src', db.Enum('web', 'api', 'im', 'mobile'))
    date = db.Column('post_date', db.DateTime)
    user_id = db.Column('post_user_id', db.Integer,
                        db.ForeignKey('users.user_id'))
    ip_int = db.Column('post_ip_int', db.Integer)
    votes = db.Column('post_votes', db.Integer)
    karma = db.Column('post_karma', db.Integer)
    content = db.Column('post_content', db.Text)
    type = db.Column('post_type', db.Enum('normal', 'admin', 'encuesta'))
    last_answer = db.Column('post_last_answer', db.DateTime)
    parent = db.Column('post_parent', db.Integer,
                       db.ForeignKey('posts.post_id'))

    children = db.relationship('Post')
    user = db.relationship('User', back_populates='posts', uselist=False)

    @property
    def public_user(self):
        if self.type == 'admin':
            return 'admin'
        return self.user.login

    def __repr__(self):
        return ('<Post %r, author %r, content %r>' %
                (self.id, self.user.login, self.content[:100]))
