from flask import request


class Menu(object):
    """so this works like this:
        if auto_endpoint is true and target is the same as request.endpoint,
        that button earns the "current" css style.
        if not, and required_kv is a tuple, we check in request.args if
        the required_kv is there."""
    def __init__(self, kind='', buttons=None, auto_endpoint=False,
                 required_key=None):
        self.kind = kind
        self.buttons = buttons if buttons else []
        self.auto_endpoint = auto_endpoint
        self.required_key = required_key

    def __iter__(self):
        for button in self.buttons:
            current = False
            if self.auto_endpoint and request.endpoint == button.endpoint:
                current = True
            if self.required_key:
                try:
                    if (request.args[self.required_key] ==
                        button.kwargs[self.required_key]):
                        current = True
                except KeyError:
                    pass
            # if we are in the same endpoint, this button has no kwargs
            # and the current request has no kwargs, assume this is the
            # "home" subview and highlight this button
            if (not self.required_key in request.args and
                    not self.required_key in button.kwargs and
                    request.endpoint == button.endpoint):
                current = True
            print("yielding: " + button.text)
            yield (button.endpoint, button.text, button.title, current,
                   button.icon, button.kwargs)


class MenuButton(object):
    def __init__(self, endpoint='#', text='', title='', icon=None, kwargs=''):
        self.endpoint = endpoint
        self.text = text
        self.title = title
        self.icon = icon
        self.kwargs = kwargs if isinstance(kwargs, dict) else {}
