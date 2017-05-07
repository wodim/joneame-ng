from datetime import datetime, timedelta
from urllib.parse import urlparse

from flask_login import current_user

from joneame.config import _cfgi
from joneame.database import db


class Link(db.Model):
    __tablename__ = 'links'

    link_id = db.Column(db.Integer, primary_key=True)
    link_author = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    link_status = db.Column(db.Enum('discard', 'queued', 'published', 'abuse',
                                    'duplicated', 'autodiscard'))
    link_randkey = db.Column(db.Integer)
    link_votes = db.Column(db.Integer)
    link_negatives = db.Column(db.Integer)
    link_anonymous = db.Column(db.Integer)
    link_votes_avg = db.Column(db.Float)
    link_comments = db.Column(db.Integer)
    link_karma = db.Column(db.Float)
    link_text = db.Column(db.Text)
    link_modified = db.Column(db.DateTime)
    link_date = db.Column(db.DateTime)
    link_sent_date = db.Column(db.DateTime)
    link_sent = db.Column(db.Boolean)
    link_category = db.Column(db.Integer,
                              db.ForeignKey('categories.category_id'))
    link_ip = db.Column(db.String(24))
    link_content_type = db.Column(db.Enum('text', 'video', 'image'))
    link_uri = db.Column(db.String(100))
    link_url = db.Column(db.String(250))
    link_url_title = db.Column(db.Text)
    link_title = db.Column(db.Text)
    link_content = db.Column(db.Text)
    link_tags = db.Column(db.Text)
    link_thumb_status = db.Column(db.Enum('unknown', 'checked', 'error',
                                          'local', 'remote', 'deleted'))
    link_thumb_x = db.Column(db.Integer)
    link_thumb_y = db.Column(db.Integer)
    link_thumb = db.Column(db.Text)
    link_comments_allowed = db.Column('link_comentarios_permitidos',
                                      db.Boolean)
    link_votes_allowed = db.Column('link_votos_permitidos', db.Boolean)
    link_broken_link = db.Column(db.Boolean)

    comments = db.relationship('Comment', back_populates='link')
    user = db.relationship('User', back_populates='links')
    category = db.relationship('Category', back_populates='links')

    clickcounter = db.relationship('ClickCounter', back_populates='link',
                                   uselist=False)
    visitcounter = db.relationship('VisitCounter', back_populates='link',
                                   uselist=False)

    def __repr__(self):
        return '<Link %r, title %r>' % (self.link_id, self.link_title[:50])

    @property
    def link_total_votes(self):
        return self.link_votes + self.link_anonymous

    @property
    def link_url_domain(self):
        netloc = urlparse(self.link_url).netloc
        if netloc[:4] == 'www.':
            netloc = netloc[4:]
        return netloc

    @property
    def is_votable(self):
        # has the user already voted?
        if self.current_user_vote:
            return False

        # can't vote on these kinds of links
        if self.link_status in ('abuse', 'autodiscard', 'duplicated'):
            return False

        # can't vote for old links
        time_enabled_votes = _cfgi('links', 'time_enabled_votes')
        if (self.link_date + timedelta(seconds=time_enabled_votes)
                < datetime.now()):
            return False

        # otherwise, can vote
        return True

    @property
    def is_votable_negative(self):
        if not current_user.is_authenticated:
            return False

        if current_user.user_id == self.link_author:
            return False

        if self.link_status in ('abuse', 'autodiscard', 'duplicated'):
            return False

        if (self.link_status == 'published' and
                self.link_date + timedelta(hours=2) > datetime.now()):
            return False

        return True

    @property
    def is_editable(self):
        user = current_user

        # admins can always edit
        if user.is_admin:
            return True

        # the user who's submitted the link can edit it for the first 15
        # minutes unless it's been published, marked as abuse, or discarded
        # by himself
        if (user.user_id == self.link_author and
                self.link_status not in ('published',
                                         'abuse',
                                         'autodiscard') and
                self.link_date + timedelta(minutes=15) < datetime.now()):
            return True

        # special users can edit for an hour after the user who submitted
        # the link can't anymore, but not if the user discarded it or it was
        # marked as abuse
        if (user.user_id != self.link_author and user.is_special and
                self.link_status not in ('abuse', 'autodiscard') and
                (self.link_date + timedelta(minutes=15) > datetime.now() and
                    self.link_date + timedelta(minutes=60) < datetime.now())):
            return True

        # otherwise, can't
        return False

    @property
    def is_map_editable(self):
        """this will suffice by now"""
        return self.is_editable

    @property
    def current_user_vote(self):
        return self.user_vote(current_user)

    def user_vote(self, user):
        """returns the Vote object of this link for the specified user (or the
            currently logged in user if user is not specified) or
            None if the user has not voted on it yet"""
        from . import Vote

        if not user.is_authenticated:
            return None

        return (
            Vote.query
            .filter(Vote.vote_type == 'links')
            .filter(Vote.vote_user_id == user.user_id)
            .filter(Vote.vote_link_id == self.link_id)
            .first()
        )

    def click(self):
        self.clickcounter.clickcounter_counter += 1
        db.session.commit()

    def visit(self):
        self.visitcounter.visitcounter_counter += 1
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.Text)
    category_lang = db.Column(db.Text)

    links = db.relationship('Link', back_populates='category')

    def __repr__(self):
        return ('<Category %r, name %r>' %
                (self.category_id, self.category_name))


class ClickCounter(db.Model):
    __tablename__ = 'link_clicks'

    clickcounter_link_id = db.Column('id', db.Integer,
                                     db.ForeignKey('links.link_id'),
                                     primary_key=True)
    clickcounter_counter = db.Column('counter', db.Integer)

    link = db.relationship('Link', back_populates='clickcounter')


class VisitCounter(db.Model):
    __tablename__ = 'link_visits'

    visitcounter_link_id = db.Column('id', db.Integer,
                                     db.ForeignKey('links.link_id'),
                                     primary_key=True)
    visitcounter_counter = db.Column('counter', db.Integer)

    link = db.relationship('Link', back_populates='visitcounter')
