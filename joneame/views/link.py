from flask import abort, render_template, request, g
from flask.ext.classy import FlaskView, route

from .sidebox import Sidebox
from ..models import LinkModel, UserModel
from ..config import _cfgi

from datetime import datetime, timedelta

class LinkView(FlaskView):
    route_base = '/'
    
    @route('/historia/<link_uri>')
    def get(self, link_uri):
        link = LinkModel.query.filter(LinkModel.link_uri == link_uri).first_or_404() # TODO revisar fecha de activacion
        
        return render_template('linkview.html', link=link)

class LinkListView(FlaskView):
    route_base = '/'

    @route('/', endpoint='LinkListView:home')
    @route('/queue/', endpoint='LinkListView:queue')
    def get(self, page=1):
        if request.endpoint == 'LinkListView:home' or request.endpoint == 'LinkListView:home_paged':
            query = LinkModel.query \
                .filter(LinkModel.link_status == 'published') \
                .order_by('link_date desc')
        if request.endpoint == 'LinkListView:queue' or request.endpoint == 'LinkListView:queue_paged':
            query = LinkModel.query \
                .filter(LinkModel.link_status == 'queued', LinkModel.link_sent_date > (datetime.utcnow() - timedelta(weeks=4))) \
                .order_by('link_date desc')
        
        try:
            page = int(request.args['page'])
        except:
            page = 1
        
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        links = pagination.items
        
        if links == None:
            abort(404)

        g.sidebar = [Sidebox.top_links()]

        return render_template('linklist.html', links=links, pagination=pagination, endpoint=request.endpoint)