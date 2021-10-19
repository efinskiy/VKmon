import datetime
from flask import Blueprint, render_template, redirect, url_for, request
from flask.globals import current_app
from flask_login.utils import login_required
from flask_login import current_user
from . import db 
from .models import User, Settings, Client, Tracking
from .custom_dec import have_add_permission, have_read_others_permission, is_admin
import subprocess
from subprocess import Popen
import os 
import logging
import signal
from sqlalchemy import or_
from psutil import pid_exists
from custom_db_func import commit, delete


admin = Blueprint('admin', __name__)

@admin.route('/service')
@login_required
@is_admin
def GET_admin():
    clients = Client.query.all()
    d_now = datetime.datetime.now().strftime('%H:%M:%S %D ')
    return render_template('admin.html', clients = clients, d_now=d_now)

@admin.route('/api/addnewtrack', methods=['POST'])
@login_required
@have_add_permission
def POST_track_new():
    target = request.form.get('target')
    d_now = datetime.datetime.now()
    adder = current_user
    new_target = commit(Client(vkid=target, tracking_enabled=1, create_time=d_now, user=adder)) 
    new_thread = subprocess.Popen(["python3.8", f"{admin.root_path}/trackbot.py", "--target", f"{target}", "--id", f"{new_target.id}"],  stdout=subprocess.DEVNULL)
    new_target.pid = new_thread.pid
    commit(new_target)
    return redirect(url_for('admin.GET_admin'))

@admin.route('/api/stop')
@login_required
@have_add_permission
def GET_track_stop():
    id = request.args.get('id')
    client = Client.query.get(int(id))
    client.tracking_enabled = 0
    commit(client)
    return redirect(request.referrer)

@admin.route('/api/start')
@login_required
@have_add_permission
def GET_track_start():
    id = request.args.get('id')
    client = Client.query.get(int(id))
    client.tracking_enabled = 1
    commit(client)
    return redirect(request.referrer)


@admin.route('/api/reboot')
@login_required
@have_add_permission
def GET_track_reboot():
    id = request.args.get('id')
    client = Client.query.get(int(id))
    try:
        os.kill(int(client.pid), signal.SIGTERM)
    except:
        pass

    new_thread = subprocess.Popen(   ["python3.8", f"{admin.root_path}/trackbot.py", "--target", f"{client.vkid}", "--id", f"{client.id}"],  stdout=subprocess.DEVNULL    )
    client.pid  = new_thread.pid
    commit(client)
    return redirect(request.referrer)



@admin.route('/api/delete')
@login_required
@have_add_permission
def GET_delete():
    id = request.args.get('id')
    client = Client.query.get(int(id))
    try:
        os.kill(int(client.pid), signal.SIGTERM)
    except:
        pass
    for row in Tracking.query.filter_by(client=client).all():
        delete(row)
        delete(client)
    return redirect(request.referrer)

@admin.route('/service/heartbeat')
@login_required
@is_admin
def GET_heartbeat():
    clients = Client.query.filter(or_(Client.tracking_enabled==1, Client.tracking_enabled==0)).all()
    a = []
    for client in clients:
        if psutil.pid_exists(int(client.pid)):
            a.append([client, 1])
        else:
            a.append([client, 0])
    return render_template('heart.html', data = a)
