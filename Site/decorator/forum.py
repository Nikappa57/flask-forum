from functools import wraps
from flask import abort
from flask_login import current_user

from Site.models.permission import Permission



def check_priority(action):
    """
        Check if currentuser priority is > of priority required
        else return abort(401)
    """
    def wrap(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.check_perm(action):
                return abort(401)

            return func(*args, **kwargs)
        return decorated_view
    return wrap