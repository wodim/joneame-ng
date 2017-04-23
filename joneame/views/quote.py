from joneame import app
from joneame.models import QuoteModel
from joneame.views.base import render_page


@app.route('/corto/<int:quote_id>', endpoint='Quote:get')
def get_quote(quote_id):
    quote = (
        QuoteModel.query
        .filter(QuoteModel.quote_id == quote_id)
        .first_or_404()
    )

    return render_page('quoteview.html', quote=quote)
