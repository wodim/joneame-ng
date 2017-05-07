from joneame.database import db


class Ban(db.Model):
    __tablename__ = 'bans'

    ban_id = db.Column(db.Integer, primary_key=True)
    ban_type = db.Column(db.Enum('email', 'punished_hostname', 'hostname',
                                 'ip', 'words', 'proxy'))
    ban_text = db.Column(db.Text)
    ban_date = db.Column(db.DateTime)
    ban_expire = db.Column(db.DateTime)
    ban_comment = db.Column(db.Text)

    def __repr__(self):
        return '<Ban %r, type %r, text %r>' % (self.ban_id, self.ban_type,
                                               self.ban_text)
