import datetime
from os import abort
from typing import Set
from flask import Blueprint, request
from datetime import datetime as dt, timedelta
import json
from . import db 
from .models import User, Settings, Client, Tracking
from .custom_dec import check_bot_auth
bapi = Blueprint('botapi', __name__)
import logging
from flask import current_app
from custom_db_func import commit


# utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
@bapi.route("/botapi/change", methods=['POST'])
@check_bot_auth
def changestatus():
    status = request.form['status']
    if status != 'online' and 'last_seen' in request.args:
        df = dt.utcfromtimestamp(int(request.args.get('last_seen')) ).strftime('%Y-%m-%d %H:%M:%S')
    else:
        df = dt.now()
        
    vid = request.form['id']
    client_obj = Client.query.get(int(vid))
    tracking_obj = Tracking.query.filter_by(client=client_obj).order_by(Tracking.date_from.desc()).first()
    if tracking_obj: 
        tracking_obj.date_to = str(dt.now())
        if tracking_obj.status == int(status):
            return json.dumps({})

    # new_tracking = Tracking(client = client_obj, date_from = dt.now(), date_to = 'now',  status=int(status))
    new_tracking = Tracking(client = client_obj, date_from = df, date_to = dt(1970, 1, 1),  status=int(status))
    commit(new_tracking)
    return json.dumps({})

@bapi.route('/botapi/status', methods=['POST'])
@check_bot_auth
def check_tracking():
    vkid = request.form['vkid']
    client = Client.query.filter_by(vkid=vkid).first()
    if client.tracking_enabled == 0:
        return json.dumps(
                            {'status': 0}
                         )
    elif client.tracking_enabled == 1:
        return json.dumps(
                            {'status': 1}
                         )
