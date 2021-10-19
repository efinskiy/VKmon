import re
from flask import session, abort, request
from functools import wraps
from .models import User, Settings
import logging
from flask.globals import current_app
from flask_login import current_user

def have_add_permission(func):
    @wraps(func)
    def wraped(*args, **kwargs):
        if not current_user.permission_add_new:
            return abort(401)
        return func(*args, **kwargs)
    return wraped

def have_read_others_permission(func):
    @wraps(func)
    def wraped(*args, **kwargs):
        if not current_user.permission_read_others:
            return abort(401)
        return func(*args, **kwargs)
    return wraped

def is_admin(func):
    @wraps(func)
    def wraped(*args, **kwargs):
        if not current_user.is_admin:
            return abort(401)
        return func(*args, **kwargs)
    return wraped

def check_bot_auth(func):
    @wraps(func)
    def wraped(*args, **kwargs):
        authkey = Settings.query.filter_by(key="botkey").first()
        if r:=request.form['botkey']:
            if r != authkey.value: return abort(401)
            return func(*args, **kwargs)
        else:
            return abort(401)
    return wraped