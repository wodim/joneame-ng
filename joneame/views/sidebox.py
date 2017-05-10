from flask import render_template
from flask_babel import gettext as _

from joneame.models import Category, Comment, Link
from joneame.database import db


def sidebox_categories():
    categories = (
        db.session.query(Category)
        .order_by(Category.name.asc())
        .all()
    )

    return render_template('sidebox/categories.html',
                           sidebox_name=_('categories'), categories=categories)


def sidebox_top_links():
    links = (
        db.session
        .query(
            Link,
            ((Link.positives + Link.anonymous - Link.negatives) *
             (1 - (db.func.unix_timestamp(db.func.now())
                   - db.func.unix_timestamp(Link.date))
              * 0.8 / 129600)).label('value')
        )
        .filter(Link.status == 'published')
        .filter(Link.date > db.func.from_unixtime(
                (db.func.unix_timestamp(db.func.now()) - 129600 * 50)))
        .order_by(db.text('value desc'))
        .limit(10)
    )

    links = [link for (link, score) in links.all()]

    if not links:
        return ''

    return render_template('sidebox/link.html', sidebox_name=_('hot links'),
                           links=links)


def sidebox_top_queued():
    links = (
        db.session.query(Link)
        .filter(Link.status == 'queued')
        .filter(Link.date > db.func.from_unixtime(
                (db.func.unix_timestamp(db.func.now()) - 86400 * 7)))
        .order_by(Link.karma.desc())
        .limit(10).all()
    )

    if not links:
        return ''

    return render_template('sidebox/link.html', sidebox_name=_('hot links'),
                           links=links)


def sidebox_last_comments():
    comments = (
        db.session.query(Comment)
        .options(db.joinedload(Comment.link))
        .options(db.joinedload(Comment.user))
        .order_by(Comment.id.desc())
        .limit(10).all()
    )

    if not comments:
        return ''

    return render_template('sidebox/comment.html',
                           sidebox_name=_('last comments'),
                           comments=comments)
