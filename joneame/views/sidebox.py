from flask import abort, render_template, request, redirect
from flask.ext.classy import FlaskView, route

from ..models import PostModel, LinkModel, UserModel
from ..config import _cfgi
from ..database import db

class Sidebox():
    @classmethod
    def top_links(self):
        query = db.session.query(LinkModel, ((LinkModel.link_votes + LinkModel.link_anonymous - LinkModel.link_negatives) * (1 - (db.func.unix_timestamp(db.func.now()) - db.func.unix_timestamp(LinkModel.link_date)) * 0.8 / 129600)).label('value')) \
                 .filter(LinkModel.link_status == 'published', LinkModel.link_date > db.func.from_unixtime((db.func.unix_timestamp(db.func.now()) - 129600 * 50))) \
                 .order_by('value desc') \
                 .limit(10).all()

        links = [x for (x, y) in query]

        return render_template('sidebox/link.html', sidebox_name='populares', links=links)

    def top_links_nsfw(self):
        pass

    def top_queued_links(self):
        pass

    def top_comments(self):
        pass

    def last_comments(self):
        pass

    def top_posts(self):
        pass