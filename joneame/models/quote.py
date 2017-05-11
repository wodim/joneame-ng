from joneame.database import db


class Quote(db.Model):
    __tablename__ = 'cortos'

    id = db.Column('id', db.Integer, primary_key=True)
    text = db.Column('texto', db.Text)
    user_id = db.Column('por', db.Integer, db.ForeignKey('users.user_id'))
    visible = db.Column('activado', db.Integer)
    votes = db.Column('votos', db.Integer)
    karma = db.Column('carisma', db.Integer)
    edits = db.Column('ediciones', db.Integer)

    def __repr__(self):
        return ('<Quote %r, user %r, text %r>' %
                (self.id, self.user.login, self.text[:300]))
