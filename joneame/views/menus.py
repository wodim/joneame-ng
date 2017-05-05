from flask import request


class Menu(object):
    def __init__(self, kind='', buttons=None,
                 default_hint=None, no_default=False):
        self.kind = kind
        self.buttons = buttons if buttons else []
        self.default_hint = default_hint
        self.no_default = no_default

    def __iter__(self):
        for button in self.buttons:
            current = False
            if self.no_default:
                pass
            elif self.default_hint:
                if self.default_hint in request.args:
                    if (self.default_hint in button.kwargs and
                            (button.kwargs[self.default_hint] ==
                             request.args[self.default_hint])):
                        current = True
                else:
                    if self.default_hint not in button.kwargs:
                        current = True
                    if button.default:
                        current = True
            else:
                if request.endpoint == button.endpoint:
                    current = True
            yield (button.endpoint, button.text, button.title, current,
                   button.icon, button.kwargs)


class MenuButton(object):
    def __init__(self, endpoint=None, text='', title='', icon=None,
                 default=False, kwargs=''):
        self.endpoint = endpoint or request.endpoint
        self.text = text
        self.title = title
        self.icon = icon
        self.default = default
        self.kwargs = kwargs if isinstance(kwargs, dict) else {}
