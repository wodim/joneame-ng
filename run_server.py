# this file is used to run the server for development purposes, NOT to
# run the server in production! you are supposed to use uwsgi and a reverse
# proxy in production!

from werkzeug.contrib.profiler import ProfilerMiddleware
from sqltap.wsgi import SQLTapMiddleware

from joneame import app


if __name__ == '__main__':
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['PROFILE'] = True

    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[10])
    app.wsgi_app = SQLTapMiddleware(app.wsgi_app)

    app.jinja_env.trim_blocks = False
    app.jinja_env.lstrip_blocks = False
    app.jinja_env.auto_reload = True

    app.run(host='0.0.0.0', port=55500, debug=True)
