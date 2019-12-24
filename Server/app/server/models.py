"""Server models."""

import enum
from datetime import datetime
from app import DB
from app.auth.models import User

class Server(DB.Model):
    """Server model."""
    __tablename__ = 'server'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String)
    path = DB.Column(DB.String)
    hash = DB.Column(DB.String)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))
    data_size = DB.Column(DB.Integer)

    def __init__(self, name, path, hash,data_size, user_id):
        self.name = name
        self.path = path
        self.hash = hash
        self.data_size = data_size
        self.user_id = user_id

    def create(cls,name,path,hash,data_size,user_id):
        server = Server(name,path,hash,data_size,user_id)
        DB.session.add(server)
        DB.session.commit()
        DB.session.refresh(server)
        return server

    def to_dict(self):
        my_dict = {}
        my_dict["id"] = self.id
        my_dict["name"] = self.name
        my_dict["path"] = self.path
        my_dict["hash"] = self.hash
        my_dict["data_size"] = self.data_size
        my_dict["user_id"] = self.user_id
        return my_dict
