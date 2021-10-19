from flask import Blueprint, session, render_template, abort, Response
from flask.globals import current_app, request
from flask.helpers import url_for
from flask_login.utils import login_required
from werkzeug.utils import redirect
import os
from .models import User, Settings, Client, Tracking
from datetime import datetime as dt
from datetime import timedelta as td
from . import db
import vk_api
from .config import vktoken

main = Blueprint('main', __name__)

api_session = vk_api.VkApi(token=vktoken)
vk = api_session.get_api()

def create_user_report(user, data):
    pass


@main.route('/')
@login_required
def root():
    return abort(404)

@main.route('/track/<id>')
def track(id):
    client = Client.query.get(id)
    tracking = Tracking.query.filter_by(client=client).filter(Tracking.date_from>dt.today()-td(days=3) ).all()
    user = vk.users.get(user_ids=client.vkid, fields='photo_max_orig', name_case='Nom', v=5.126)
    return render_template('tracking.html', client=client, date=dt.now(), tracking=tracking, photo_url=user[0]['photo_max_orig'])