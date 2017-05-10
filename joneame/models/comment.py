from joneame.database import db


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column('comment_id', db.Integer, primary_key=True)
    type = db.Column('comment_type', db.Enum('normal', 'especial', 'admin'))
    randkey = db.Column('comment_randkey', db.Integer)
    link_id = db.Column('comment_link_id', db.Integer,
                        db.ForeignKey('links.link_id'))
    user_id = db.Column('comment_user_id', db.Integer,
                        db.ForeignKey('users.user_id'))
    date = db.Column('comment_date', db.DateTime)
    ip = db.Column('comment_ip', db.String(24))
    order = db.Column('comment_order', db.Integer)
    votes = db.Column('comment_votes', db.Integer)
    karma = db.Column('comment_karma', db.Integer)
    content = db.Column('comment_content', db.Text)

    link = db.relationship('Link', back_populates='comments')

    def __repr__(self):
        return ('<Comment %r, user %r, content %r>' %
                (self.id, self.user.login,
                 self.content[:100]))
