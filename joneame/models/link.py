from datetime import datetime, timedelta
from urllib.parse import urlparse

from flask_login import current_user

from joneame.config import _cfgi
from joneame.database import db


class Link(db.Model):
    __tablename__ = 'links'

    id = db.Column('link_id', db.Integer, primary_key=True)
    author = db.Column('link_author', db.Integer,
                       db.ForeignKey('users.user_id'))
    status = db.Column('link_status',
                       db.Enum('discard', 'queued', 'published', 'abuse',
                               'duplicated', 'autodiscard'))
    randkey = db.Column('link_randkey', db.Integer)
    positives = db.Column('link_votes', db.Integer)
    negatives = db.Column('link_negatives', db.Integer)
    anonymous = db.Column('link_anonymous', db.Integer)
    votes_avg = db.Column('link_votes_avg', db.Float)
    comment_count = db.Column('link_comments', db.Integer)
    karma = db.Column('link_karma', db.Float)
    text = db.Column('link_text', db.Text)
    modified = db.Column('link_modified', db.DateTime)
    date = db.Column('link_date', db.DateTime)
    sent_date = db.Column('link_sent_date', db.DateTime)
    sent = db.Column('link_sent', db.Boolean)
    category_id = db.Column('link_category', db.Integer,
                            db.ForeignKey('categories.category_id'))
    ip = db.Column('link_ip', db.String(24))
    content_type = db.Column('link_content_type',
                             db.Enum('text', 'video', 'image'))
    uri = db.Column('link_uri', db.String(100))
    url = db.Column('link_url', db.String(250))
    url_title = db.Column('link_url_title', db.Text)
    title = db.Column('link_title', db.Text)
    content = db.Column('link_content', db.Text)
    tags = db.Column('link_tags', db.Text)
    thumb_status = db.Column('link_thumb_status',
                             db.Enum('unknown', 'checked', 'error', 'local',
                                     'remote', 'deleted'))
    thumb_x = db.Column('link_thumb_x', db.Integer)
    thumb_y = db.Column('link_thumb_y', db.Integer)
    thumb = db.Column('link_thumb', db.Text)
    comments_allowed = db.Column('link_comentarios_permitidos', db.Boolean)
    votes_allowed = db.Column('link_votos_permitidos', db.Boolean)
    broken_link = db.Column('link_broken_link', db.Boolean)

    comments = db.relationship('Comment', back_populates='link')
    user = db.relationship('User', back_populates='links')
    category = db.relationship('Category', back_populates='links')

    clickcounter = db.relationship('ClickCounter', back_populates='link',
                                   uselist=False)
    visitcounter = db.relationship('VisitCounter', back_populates='link',
                                   uselist=False)

    def __repr__(self):
        return '<Link %r, title %r>' % (self.id, self.title[:50])

    @property
    def total_votes(self):
        return self.positives + self.anonymous

    @property
    def url_domain(self):
        netloc = urlparse(self.url).netloc
        if netloc[:4] == 'www.':
            netloc = netloc[4:]
        return netloc

    @property
    def is_votable(self):
        # can't vote on these kinds of links
        if self.status in ('abuse', 'autodiscard', 'duplicated'):
            return False

        # can't vote for old links
        time_enabled_votes = _cfgi('links', 'time_enabled_votes')
        if (self.date + timedelta(seconds=time_enabled_votes)
                < datetime.now()):
            return False

        # otherwise, can vote
        return True

    @property
    def is_votable_slow(self):
        """only to be called for contextless purposes. in templates, use
            is_votable"""
        return self.is_votable and not self._current_user_vote

    @property
    def is_votable_negative(self):
        if not current_user.is_authenticated:
            return False

        if current_user.id == self.author:
            return False

        if self.status in ('abuse', 'autodiscard', 'duplicated'):
            return False

        if (self.status == 'published' and
                self.date + timedelta(hours=2) > datetime.now()):
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
        if (user.id == self.author and
                self.status not in ('published', 'abuse', 'autodiscard') and
                self.date + timedelta(minutes=15) < datetime.now()):
            return True

        # special users can edit for an hour after the user who submitted
        # the link can't anymore, but not if the user discarded it or it was
        # marked as abuse
        if (user.id != self.author and user.is_special and
                self.status not in ('abuse', 'autodiscard') and
                (self.date + timedelta(minutes=15) > datetime.now() and
                    self.date + timedelta(minutes=60) < datetime.now())):
            return True

        # otherwise, can't
        return False

    @property
    def is_map_editable(self):
        """this will suffice by now"""
        return self.is_editable

    @property
    def _current_user_vote(self):
        return self.user_vote(current_user)

    def _user_vote(self, user):
        """returns the Vote object of this link for the specified user (or the
            currently logged in user if user is not specified) or
            None if the user has not voted on it yet"""
        from . import Vote

        if not user.is_authenticated:
            return None

        return (
            Vote.query
            .filter(Vote.type == 'links')
            .filter(Vote.user_id == user.id)
            .filter(Vote.thing_id == self.id)
            .first()
        )

    def click(self):
        self.clickcounter.counter += 1
        db.session.commit()

    def visit(self):
        self.visitcounter.counter += 1
        db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column('category_id', db.Integer, primary_key=True)
    name = db.Column('category_name', db.Text)
    lang = db.Column('category_lang', db.Text)

    links = db.relationship('Link', back_populates='category')

    def __repr__(self):
        return ('<Category %r, name %r>' %
                (self.id, self.name))


class ClickCounter(db.Model):
    __tablename__ = 'link_clicks'

    link_id = db.Column('id', db.Integer, db.ForeignKey('links.link_id'),
                        primary_key=True)
    counter = db.Column('counter', db.Integer)

    link = db.relationship('Link', back_populates='clickcounter')


class VisitCounter(db.Model):
    __tablename__ = 'link_visits'

    link_id = db.Column('id', db.Integer, db.ForeignKey('links.link_id'),
                        primary_key=True)
    counter = db.Column('counter', db.Integer)

    link = db.relationship('Link', back_populates='visitcounter')
