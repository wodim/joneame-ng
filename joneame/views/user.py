from flask import abort, render_template
from flask.ext.classy import FlaskView, route

from ..models import UserModel

class UserView(FlaskView):
    route_base = '/'
    
    @route('/mafioso/<user_login>')
    def get(self, user_login):
        user = UserModel.query.filter(UserModel.user_login == user_login).first_or_404() # revisar fecha de activacion
            
        return render_template('user.html', user=user)