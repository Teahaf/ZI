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

def ticks():
    dt = datetime.now()
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

@se.route("/get-file/<id>", methods=["GET"])
def get_file(id):
    server = Server.query.filter_by(id = id).first()
    import io
    if server:
        with io.open(server.path, "r", encoding="utf-8") as f:
            data = f.read().replace('\n', '')
    if server:
        return {"data": data,
                "hash": server.hash}
    else:
        {}

@se.route('/add-file/<id>', methods=["POST"])
def add_file(id):
    files = Server.query.filter_by(user_id = id).all()
    alocated_memory = 0
    for filee in files:
        alocated_memory += filee.data_size
    user = User.query.filter_by(id = id).first()
    uploaded_data = get_data()
    if (alocated_memory + uploaded_data.get("size"))< user.max_size:
        name = uploaded_data.get("name")
        flag = 0
        for filee in files:
            if name == filee.name:
                flag+=1
        if flag > 0:
            name= name + "(" +  str(flag) + ")"
        path = "C:\\Users\\Hafner\\Desktop\\ZI\\Server\\Files\\" + name + ticks()
        import io
        with io.open(path, "a+", encoding="utf-8") as f:
            f.write(uploaded_data.get("data"))
        server = Server.create(Server, name, path, uploaded_data.get("hash"),uploaded_data.get("size"),id)
    else:
        return "Prevaziso si maximalnu dozvoljenu kolicinu podataka."
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