from flask import request
from flask_login import AnonymousUserMixin, UserMixin


class CommonUserMixin(object):
    @property
    def remote_ip(self):
        ip = request.environ.get('REMOTE_ADDR')
        if ip and ip is not '127.0.0.1':
            return ip
        return '0.0.0.0'  # fallback


class MyUserMixin(UserMixin, CommonUserMixin):
    pass


class MyAnonymousUserMixin(AnonymousUserMixin, CommonUserMixin):
    @property
    def is_admin(self):
        return False

    @property
    def id(self):
        return 0
