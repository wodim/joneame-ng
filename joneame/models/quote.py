from ..database import db


class QuoteModel(db.Model):
    __tablename__ = 'cortos'

    quote_id = db.Column('id', db.Integer, primary_key=True)
    quote_text = db.Column('texto', db.Text)
    quote_author = db.Column('por', db.Integer, db.ForeignKey('users.user_id'))
    quote_visible = db.Column('activado', db.Integer)
    quote_votes = db.Column('votos', db.Integer)
    quote_karma = db.Column('carisma', db.Integer)
    quote_edits = db.Column('ediciones', db.Integer)

    def __repr__(self):
        return ('<Quote %r, user %r, text %r>' %
                (self.quote_id, self.user.user_login, self.quote_text[:300]))
