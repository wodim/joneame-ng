from datetime import datetime, timedelta

from flask_babel import gettext as _
from flask_login import current_user
from flask_sqlalchemy import Pagination

from joneame.config import _cfgi
from joneame.database import db
from joneame.models import Category, ClickCounter, Link, User, Vote
from joneame.views.menus import MenuButton, Menu
from joneame.views.sidebox import (sidebox_categories, sidebox_top_links,
                                   sidebox_last_comments, sidebox_top_queued)
from joneame.utils import arg_to_timedelta


class LinkList(object):
    query = None

    # filter to be applied to the links table, separated for counting purposes,
    # i.e., this way there's no need to apply joins or orders to what simply
    # is a count()
    filter_ = None

    count = None

    # parts of the page
    submenu = None
    toolbox = None
    pagination = None
    title = None
    sidebar = None
    items = None

    # state
    page = 1
    page_size = 0

    def __init__(self):
        self.items = []

        self.query = db.session.query(Link, Vote)

        buttons = [
            MenuButton(endpoint='Link:list_home', text=_('home'),),
            MenuButton(endpoint='Link:list_top', text=_('top links'),
                       kwargs={'range': '24h'}),
            MenuButton(endpoint='Link:list_top_clicks', text=_('most clicked'),
                       kwargs={'range': '24h'}),
            MenuButton(endpoint='Link:list_random', text=_('random')),
            MenuButton(endpoint='Link:list_queue', text=_('queued links')),
        ]
        self.submenu = Menu(buttons=buttons)

        self.page_size = _cfgi('misc', 'page_size')

    def fetch(self):
        numeric_ip = db.func.inet_aton(current_user.remote_ip)
        if current_user.is_authenticated:
            vote_cond = db.or_(Vote.user_id == current_user.id,
                               Vote.ip_int == numeric_ip)
        else:
            vote_cond = (Vote.ip_int == numeric_ip)

        self.count = db.session.query(Link).filter(self.filter_).count()

        self.query = (
            self.query
            .filter(self.filter_)
            .options(db.joinedload(Link.user).joinedload(User.avatar))
            .options(db.joinedload(Link.category))
            .options(db.joinedload(Link.clickcounter))
            .options(db.joinedload(Link.visitcounter))
            .outerjoin(Vote, db.and_(Vote.thing_id == Link.id,
                                     Vote.type == 'links',
                                     vote_cond))
        )

        # apply limit/offset to the query manually
        start = self.page_size * (self.page - 1)
        end = start + self.page_size
        res = self.query.slice(start, end).all()

        # populate the current_vote field of every link if it exists
        for link, vote in res:
            link.current_vote = vote
            self.items.append(link)

        self.pagination = Pagination(query=self.query, page=self.page,
                                     per_page=self.page_size, total=self.count,
                                     items=self.items)


class SingleLink(LinkList):
    """this one is a big hack so there's some fancy stuff going on"""
    def __init__(self, link_id=None, link_uri=None):
        super().__init__()

        if not link_id and not link_uri:
            raise ValueError('either link_id or link_uri are required')

        if link_id:
            self.filter_ = (Link.id == link_id)
        elif link_uri:
            self.filter_ = (Link.uri == link_uri)

        # force this to be one so we don't mess up in comment pages
        self.page = 1


class HomeLinkList(LinkList):
    def __init__(self):
        super().__init__()

        self.filter_ = (Link.status == 'published')
        self.query = self.query.order_by(Link.published_date.desc())

        self.sidebar = [sidebox_top_links, sidebox_categories,
                        sidebox_last_comments]


class QueuedLinkList(LinkList):
    def __init__(self, meta):
        super().__init__()

        if meta == 'discarded':
            self.filter_ = ~(Link.status.in_(('published', 'queued')))
            self.title = _('Discarded')
        else:
            self.filter_ = db.and_(
                (Link.date > (datetime.utcnow() - timedelta(weeks=8))),
                (Link.status == 'queued')
            )
            self.title = _('Queued')

        self.query = self.query.order_by(Link.date.desc())

        buttons = [
            MenuButton(text=_('all')),
            MenuButton(text=_('discarded'), icon='trash',
                       kwargs={'meta': 'discarded'}),
        ]
        self.toolbox = Menu(buttons=buttons, default_hint='meta')

        self.sidebar = [sidebox_top_queued, sidebox_categories]


class CategoryLinkList(LinkList):
    def __init__(self, category_id):
        super().__init__()

        category = (
            Category.query
            .filter(Category.id == category_id)
        ).first()

        if not category:
            raise KeyError('No such category')

        self.filter_ = db.and_(
            (Link.status == 'published'),
            (Link.category_id == category_id)
        )

        self.query = self.query.order_by(Link.published_date.desc())

        self.title = _('Category: %(cat_name)s',
                       cat_name=category.name)

        self.sidebar = [sidebox_top_links, sidebox_categories,
                        sidebox_last_comments]


class TopLinkList(LinkList):
    def __init__(self, range):
        super().__init__()

        buttons = [
            MenuButton(text=_('one day'), kwargs={'range': '24h'}),
            MenuButton(text=_('two days'), kwargs={'range': '48h'}),
            MenuButton(text=_('one week'), kwargs={'range': '1w'}),
            MenuButton(text=_('one month'), kwargs={'range': '1m'}),
            MenuButton(text=_('one year'), kwargs={'range': '1y'}),
            MenuButton(text=_('the beginning of time'),
                       kwargs={'range': 'all'}, default=True),
        ]
        self.toolbox = Menu(buttons=buttons, default_hint='range')

        # apply range
        td = arg_to_timedelta(range)
        if td:
            self.filter_ = db.and_(Link.status == 'published',
                                   (Link.date > datetime.now() - td))
        else:
            self.filter_ = (Link.status == 'published')

        self.title = _('Top links')

        self.sidebar = [sidebox_top_links, sidebox_categories,
                        sidebox_last_comments]


class TopVotesLinkList(TopLinkList):
    def __init__(self, range):
        super().__init__(range)

        self.query = (
            self.query
            .order_by(Link.positives + Link.anonymous.desc())
        )

        self.title = _('Top links')


class TopClicksLinkList(TopLinkList):
    def __init__(self, range):
        super().__init__(range)

        self.query = (
            self.query
            .outerjoin(Link.clickcounter)
            .order_by(ClickCounter.counter.desc())
        )

        self.title = _('Most clicked')


class RandomLinkList(LinkList):
    def __init__(self):
        super().__init__()

        link_ids = [x for y in (
                        db.session.query(Link.id)
                        .order_by(db.func.rand())
                        .limit(self.page_size).all()
                    ) for x in y]

        self.filter_ = (Link.id.in_(link_ids))

        self.title = _('Random links')


class UserLinkList(LinkList):
    def __init__(self, user_id):
        super().__init__()

        self.filter_ = (Link.user_id == user_id)
        self.query = self.query.order_by(Link.date.desc())
