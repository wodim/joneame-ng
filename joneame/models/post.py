from ..database import db

class PostModel(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    post_randkey = db.Column(db.Integer)
    post_src = db.Column(db.Enum(['web', 'api', 'im', 'mobile']))
    post_date = db.Column(db.DateTime)
    post_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_ip_int = db.Column(db.Integer)
    post_votes = db.Column(db.Integer)
    post_karma = db.Column(db.Integer)
    post_content = db.Column(db.Text)
    post_type = db.Column(db.Enum(['normal', 'admin', 'poll']))
    post_parent = db.Column(db.Integer, db.ForeignKey('posts.post_id'))

    children = db.relationship('PostModel') # , primaryjoin='and_(PostModel.post_id==PostModel.post_parent, PostModel.post_parent==0)')

    def __repr__(self):
        return '<Post %r, author %r, content %r>' % (self.post_id, self.user.user_login, self.post_content[:100])