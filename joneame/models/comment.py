from joneame.database import db


class CommentModel(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    comment_type = db.Column(db.Enum('normal', 'especial', 'admin'))
    comment_randkey = db.Column(db.Integer)
    comment_link_id = db.Column(db.Integer, db.ForeignKey('links.link_id'))
    comment_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment_date = db.Column(db.DateTime)
    comment_ip = db.Column(db.String(24))
    comment_order = db.Column(db.Integer)
    comment_votes = db.Column(db.Integer)
    comment_karma = db.Column(db.Integer)
    comment_content = db.Column(db.Text)

    def __repr__(self):
        return ('<Comment %r, user %r, content %r>' %
                (self.comment_id, self.user.user_login,
                 self.comment_content[:100]))
