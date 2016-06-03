from flask import render_template
from flask_classy import FlaskView, route

from ..models import QuoteModel
from ..database import db

from random import randint

def random_quote():
    quote_max = db.session.query(db.func.max(QuoteModel.quote_id)).first()[0]
    quote = QuoteModel.query.filter(QuoteModel.quote_id > randint(0, quote_max)).first()

    return quote

class QuoteView(FlaskView):
    route_base = '/'

    @route('/corto/<int:quote_id>')
    def get(self, quote_id):
        quote = QuoteModel.query.filter(QuoteModel.quote_id == quote_id).first_or_404()

        return render_template('quoteview.html', quote=quote)