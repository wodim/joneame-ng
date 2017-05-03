from flask import request


class Menu(object):
    def __init__(self, kind='', buttons=None, auto_endpoint=False,
                 default_hint=None):
        self.kind = kind
        self.buttons = buttons if buttons else []
        self.auto_endpoint = auto_endpoint
        self.default_hint = default_hint

    def __iter__(self):
        for button in self.buttons:
            current = False
            if self.auto_endpoint:
                if request.endpoint == button.endpoint:
                    current = True
            else:
                if self.default_hint and self.default_hint in request.args:
                    try:
                        if (request.args[self.default_hint] ==
                                button.kwargs[self.default_hint]):
                            current = True
                    except KeyError:
                        pass
                elif (self.default_hint not in request.args and
                        self.default_hint not in button.kwargs):
                    current = True
                elif button.default:
                    current = True
            yield (button.endpoint, button.text, button.title, current,
                   button.icon, button.kwargs)


class MenuButton(object):
    def __init__(self, endpoint='#', text='', title='', icon=None,
                 default=False, kwargs=''):
        self.endpoint = endpoint
        self.text = text
        self.title = title
        self.icon = icon
        self.default = default
        self.kwargs = kwargs if isinstance(kwargs, dict) else {}
