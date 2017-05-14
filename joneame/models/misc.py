from joneame.database import db


class Annotation(db.Model):
    __tablename__ = 'annotations'

    key = db.Column('annotation_key', db.String(40), primary_key=True)
    date = db.Column('annotation_time', db.DateTime)
    text = db.Column('annotation_text', db.Text)

    def __repr__(self):
        return '<Annotation %r, date %r>' % (self.key, self.date)


class Ban(db.Model):
    __tablename__ = 'bans'

    id = db.Column('ban_id', db.Integer, primary_key=True)
    kind = db.Column('ban_type',
                     db.Enum('email', 'punished_hostname', 'hostname', 'ip',
                             'words', 'proxy'))
    text = db.Column('ban_text', db.Text)
    date = db.Column('ban_date', db.DateTime)
    expire = db.Column('ban_expire', db.DateTime)
    comment = db.Column('ban_comment', db.Text)

    def __repr__(self):
        return '<Ban %r, type %r, text %r>' % (self.id, self.type, self.text)


class Clon(db.Model):
    __tablename__ = 'clones'

    from_ = db.Column('clon_from', db.Integer, primary_key=True)
    to = db.Column('clon_to', db.Integer, primary_key=True)
    ip = db.Column('clon_ip', db.Text)
    date = db.Column('clon_date', db.DateTime)

    def __repr__(self):
        return ('<Clon from %r to %r, ip %r>' %
                (self.from_, self.to, self.ip))
