from flask import abort, render_template, request, redirect
from flask.ext.classy import FlaskView, route

from ..models import QuoteModel, UserModel
from ..config import _cfgi
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