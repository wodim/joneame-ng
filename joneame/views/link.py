from flask import abort, render_template, request, g
from flask_classy import FlaskView, route

from .sidebox import Sidebox
from ..models import LinkModel, UserModel, CommentModel
from ..config import _cfgi

from datetime import datetime, timedelta

class LinkView(FlaskView):
    route_base = '/'

    @route('/historia/<link_uri>')
    def get(self, link_uri):
        link = LinkModel.query.filter(LinkModel.link_uri == link_uri).first_or_404() # TODO revisar fecha de activacion

        query = CommentModel.query.filter(CommentModel.comment_link_id == link.link_id)
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        comments = pagination.items

        return render_template('link/linkview.html', link=link, comments=comments,
                                    pagination=pagination,
                                    endpoint=request.endpoint)

class LinkListView(FlaskView):
    route_base = '/'

    @route('/', endpoint='LinkListView:home')
    @route('/queue/', endpoint='LinkListView:queue')
    def get(self, page=1):
        query = LinkModel.query
        if request.endpoint == 'LinkListView:home':
            query = query.filter(LinkModel.link_status == 'published')
        elif request.endpoint == 'LinkListView:queue':
            query = query.filter(LinkModel.link_status == 'queued')
            query = query.filter(LinkModel.link_sent_date > (datetime.utcnow() - timedelta(weeks=4)))

        query = query.order_by('link_date desc')
        page = request.args.get('page', 1, type=int)
        pagination = query.paginate(page, _cfgi('misc', 'page_size'))
        links = pagination.items

        if not links:
            abort(404)

        g.sidebar = [Sidebox.top_links(), Sidebox.last_comments()]

        return render_template('link/linklist.html', links=links,
                                    pagination=pagination,
                                    endpoint=request.endpoint)
