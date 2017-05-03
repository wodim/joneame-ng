from flask import redirect, url_for
from flask_babel import gettext as _

from joneame import app
from joneame.database import db
from joneame.models import Quote, User
from joneame.views.base import get_random_quote, render_page
from joneame.views.menus import Menu, MenuButton


@app.route('/corto/<int:quote_id>', endpoint='Quote:get')
def get_quote(quote_id):
    quote = (
        Quote.query
        .options(db.joinedload(Quote.user).joinedload(User.avatar))
        .filter(Quote.quote_id == quote_id)
        .first_or_404()
    )

    buttons = [
        MenuButton(endpoint='Quote:random_redir', text=_('new quote'),
                   icon='plus-square'),
        MenuButton(endpoint='Quote:random_redir', text=_('random quote'),
                   icon='refresh'),
    ]
    toolbox = Menu(buttons=buttons, no_default=True)

    return render_page('user/quoteview.html', quote=quote,
                       quote_toolbox=toolbox, show_quote=False)


@app.route('/cortos', endpoint='Quote:random_redir')
def random_quote_redir():
    random_quote_id = get_random_quote().quote_id
    return redirect(url_for('Quote:get', quote_id=random_quote_id))
