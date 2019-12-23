"""Auth routes."""

import traceback
import random
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from flask_cors import cross_origin
from app.auth import authentication as at
from datetime import datetime
from app import DB as db
from app.auth.models import User
from app.server import server as se
from app.server import Server

def ticks(self):
    dt = self.ticks(datetime.now())
    t = (dt - datetime(1, 1, 1)).total_seconds() * 10000000
    return str(t)

def get_data():
    """Get data from request."""
    data = None
    try:
        data = request.json
        if data == {}:
            data = request.data
    except:
        traceback.print_exc()
        data = {}

    return data

@se.route('/add-file/<id>', methods=["POST"])
def add_file(id):
    data = get_data()
    name = data.get("name")
    path = "C:\\Users\\Hafner\\Desktop\\ZI\\Server\\Files\\" + name
    import io
    with io.open(path, "a+", encoding="utf-8") as f:
        f.write(data.get("data"))
    print(path)
    print(name)
    server = Server.create(Server, name, path , id)

    if server:
        return server.to_dict()
    else:
        return {}

@se.route('/get-files/<id>', methods=["GET"])
def get_files_for_user(id):
    files = Server.query.filter_by(user_id = id).all()
    dicts = []
    for filee in files:
        dicts.append(filee.to_dict())
    return dicts

@se.after_request
def creds(response):
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response