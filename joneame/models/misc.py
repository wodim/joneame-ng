from joneame.database import db


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.Text)
    category_lang = db.Column(db.Text)

    links = db.relationship('Link', back_populates='category', lazy='select')

    def __repr__(self):
        return ('<Category %r, name %r>' %
                (self.category_id, self.category_name))