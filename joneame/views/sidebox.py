from flask import render_template
from flask_babel import gettext as _

from joneame.models import CategoryModel, CommentModel, LinkModel
from joneame.database import db


def sidebox_categories():
    categories = (
        db.session.query(CategoryModel)
        .order_by('category_name asc')
        .all()
    )

    return render_template('sidebox/categories.html',
                           sidebox_name=_('categories'), categories=categories)


def sidebox_top_links():
    links = (
        db.session
        .query(
            LinkModel,
            ((LinkModel.link_votes + LinkModel.link_anonymous
              - LinkModel.link_negatives) *
             (1 - (db.func.unix_timestamp(db.func.now())
                   - db.func.unix_timestamp(LinkModel.link_date))
              * 0.8 / 129600)).label('value')
        )
        .filter(LinkModel.link_status == 'published')
        .filter(LinkModel.link_date > db.func.from_unixtime(
                (db.func.unix_timestamp(db.func.now()) - 129600 * 50)))
        .order_by('value desc')
        .limit(10)
    )

    links = [link for (link, score) in links.all()]

    return render_template('sidebox/link.html', sidebox_name=_('hot links'),
                           links=links)


def sidebox_top_queued():
    links = (
        db.session.query(LinkModel)
        .filter(LinkModel.link_status == 'queued')
        .filter(LinkModel.link_date > db.func.from_unixtime(
                (db.func.unix_timestamp(db.func.now()) - 86400 * 7)))
        .order_by(LinkModel.link_karma.desc())
        .limit(10)
    )

    return render_template('sidebox/link.html', sidebox_name=_('hot links'),
                           links=links)


def sidebox_last_comments():
    comments = (
        db.session.query(CommentModel)
        .order_by('comment_id desc')
        .limit(10).all()
    )

    return render_template('sidebox/comment.html',
                           sidebox_name=_('last comments'),
                           comments=comments)
