from flask import abort, render_template, request, redirect
from flask_classy import FlaskView, route

from ..models import PostModel, LinkModel, UserModel, CommentModel
from ..config import _cfgi
from ..database import db

class Sidebox():
    @classmethod
    def top_links(self):
        query = db.session.query(LinkModel,
                ((LinkModel.link_votes + LinkModel.link_anonymous
                    - LinkModel.link_negatives) *
                (1 - (db.func.unix_timestamp(db.func.now())
                    - db.func.unix_timestamp(LinkModel.link_date))
                        * 0.8 / 129600)).label('value')) \
                .filter(LinkModel.link_status == 'published',
                    LinkModel.link_date
                        > db.func.from_unixtime(
                            (db.func.unix_timestamp(db.func.now())
                                                    - 129600 * 50))) \
                .order_by('value desc') \
                .limit(10)

        links = [x for (x, y) in query.all()]

        return render_template('sidebox/link.html',
                               sidebox_name='hot links',
                               links=links)

    @classmethod
    def top_links_nsfw(self):
        pass

    @classmethod
    def top_queued_links(self):
        pass

    @classmethod
    def top_comments(self):
        pass

    @classmethod
    def last_comments(self):
        comments = db.session.query(CommentModel).order_by('comment_id desc').limit(10).all()

        return render_template('sidebox/comment.html',
                               sidebox_name='last comments',
                               comments=comments)

    @classmethod
    def top_posts(self):
        pass
