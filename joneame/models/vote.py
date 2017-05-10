from joneame.database import db


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column('vote_id', db.Integer, primary_key=True)
    type = db.Column('vote_type', db.Enum('links', 'comments', 'posts',
                                          'cortos', 'poll_comment'))
    date = db.Column('vote_date', db.DateTime)
    thing_id = db.Column('vote_link_id', db.Integer)
    user_id = db.Column('vote_user_id', db.Integer,
                        db.ForeignKey('users.user_id'))
    value = db.Column('vote_value', db.Integer)
    ip_int = db.Column('vote_ip_int', db.Integer)  # !!!
    random = db.Column('vote_aleatorio', db.Enum('normal', 'aleatorio'))

    user = db.relationship('User', back_populates='votes', uselist=False)

    @property
    def parent(self):
        return getattr(self, 'parent_%s' % self.discriminator)

    def __repr__(self):
        return ('<Vote %r, type %r, user %r, ip_int %r, thing %r, value %r>' %
                (self.id, self.type, self.user_id, self.ip_int,
                 self.thing_id, self.value))
