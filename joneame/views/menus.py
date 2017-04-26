from flask import request


class Menu(object):
    """so this works like this:
        if auto_endpoint is true and target is the same as request.endpoint,
        that button earns the "current" css style. that's it.
        if not, and required_key is present, if required_key is present in
        request.args and equals the value of a certain button, that button
        is marked as current.
        if not, and required_key is present, but it is not present in
        request.args, and the current button has no required_key,
        that button is marked as current. that means that no more than one
        button can have no required_key."""
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
            if (self.required_key not in request.args and
                    self.required_key not in button.kwargs and
                    request.endpoint == button.endpoint):
                current = True
            yield (button.endpoint, button.text, button.title, current,
                   button.icon, button.kwargs)


class MenuButton(object):
    def __init__(self, endpoint='#', text='', title='', icon=None, kwargs=''):
        self.endpoint = endpoint
        self.text = text
        self.title = title
        self.icon = icon
        self.kwargs = kwargs if isinstance(kwargs, dict) else {}
