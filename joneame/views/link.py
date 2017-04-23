from flask import abort, request

from joneame import app
from joneame.views.base import render_page
from joneame.models import LinkModel, CommentModel
from joneame.config import _cfgi

from datetime import datetime, timedelta


@app.route('/<link_uri>', endpoint='Link:get')
def get_link(link_uri):
    link = (
        LinkModel.query
        .filter(LinkModel.link_uri == link_uri)
        .first_or_404()
    )  # TODO revisar fecha de activacion

    comments = (
        CommentModel.query
        .filter(CommentModel.comment_link_id == link.link_id)
    )
    page = request.args.get('page', 1, type=int)
    pagination = comments.paginate(page, _cfgi('misc', 'page_size'))
    comments = pagination.items

    return render_page('link/linkview.html', link=link, comments=comments,
                       pagination=pagination,
                       endpoint=request.endpoint)


@app.route('/', endpoint='Link:list_home')
@app.route('/queue/', endpoint='Link:list_queue')
def get_link_list(page=1):
    query = LinkModel.query
    if request.endpoint == 'Link:list_home':
        query = query.filter(LinkModel.link_status == 'published')
    elif request.endpoint == 'Link:list_queue':
        query = query.filter(LinkModel.link_status == 'queued')
        query = query.filter(LinkModel.link_sent_date
                             > (datetime.utcnow() - timedelta(weeks=4)))

    query = query.order_by(LinkModel.link_sent_date.desc())
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page, _cfgi('misc', 'page_size'))
    links = pagination.items

    if not links:
        abort(404)

    return render_page('link/linklist.html', links=links,
                       pagination=pagination,
                       endpoint=request.endpoint)
