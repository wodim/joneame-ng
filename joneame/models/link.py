from ..database import db

class LinkModel(db.Model):
    __tablename__ = 'links'

    link_id = db.Column(db.Integer, primary_key=True)
    link_author = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    link_status = db.Column(db.Enum(['discard', 'queued', 'published', 'abuse', 'duplicated', 'autodiscard']))
    link_randkey = db.Column(db.Integer)
    link_votes = db.Column(db.Integer)
    link_negatives = db.Column(db.Integer)
    link_anonymous = db.Column(db.Integer)
    link_votes_avg = db.Column(db.Float)
    link_comments = db.Column(db.Integer)
    link_karma = db.Column(db.Float)
    link_text = db.Column(db.Text)
    link_modified = db.Column(db.DateTime)
    link_date = db.Column(db.DateTime)
    link_sent_date = db.Column(db.DateTime)
    link_sent = db.Column(db.Boolean)
    link_category = db.Column(db.Integer) # falta relacion
    link_ip = db.Column(db.String(24))
    link_content_type = db.Column(db.Enum(['text', 'video', 'image']))
    link_uri = db.Column(db.String(100))
    link_url = db.Column(db.String(250))
    link_url_title = db.Column(db.Text)
    link_title = db.Column(db.Text)
    link_content = db.Column(db.Text)
    link_tags = db.Column(db.Text)
    link_thumb_status = db.Column(db.Enum(['unknown', 'checked', 'error', 'local', 'remote', 'deleted']))
    link_thumb_x = db.Column(db.Integer)
    link_thumb_y = db.Column(db.Integer)
    link_thumb = db.Column(db.Text)
    link_comentarios_permitidos = db.Column(db.Boolean)
    link_votos_permitidos = db.Column(db.Boolean)
    link_broken_link = db.Column(db.Boolean)

    comments = db.relationship('CommentModel', backref='link', lazy="dynamic")

    def __repr__(self):
        return '<Link %r, author %r>' % (self.link_id, self.link_author)