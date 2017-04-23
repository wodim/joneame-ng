from flask import render_template

from ..models import LinkModel, CommentModel
from ..database import db


def sidebox_top_links():
    links = (
        db.session.query(
            LinkModel,
            (LinkModel.link_votes + LinkModel.link_anonymous
             - LinkModel.link_negatives) *
            (1 - (db.func.unix_timestamp(db.func.now())
                  - db.func.unix_timestamp(LinkModel.link_date))
             * 0.8 / 129600)
            .label('value')
        )
        .filter(LinkModel.link_status == 'published')
        .filter(LinkModel.link_date > db.func.from_unixtime(
                (db.func.unix_timestamp(db.func.now()) - 129600 * 50)))
        .order_by('value desc')
        .limit(10)
        )

    links = [x for (x, y) in links.all()]

    return render_template('sidebox/link.html', sidebox_name='hot links',
                           links=links)


def sidebox_last_comments():
    comments = (
        db.session.query(CommentModel)
        .order_by('comment_id desc')
        .limit(10).all()
    )

    return render_template('sidebox/comment.html',
                           sidebox_name='last comments',
                           comments=comments)
