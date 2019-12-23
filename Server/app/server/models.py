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
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"))

    def __init__(self, name, path, user_id):
        self.name = name
        self.path = path
        self.user_id = user_id

    def create(cls,name,path,user_id):
        print(name)
        print(path)
        print(user_id)
        server = Server(name,path,user_id)
        print(server.name)
        DB.session.add(server)
        DB.session.commit()
        DB.session.refresh(server)
        print(server.to_dict())
        return server

    def to_dict(self):
        my_dict = {}
        my_dict["id"] = self.id
        my_dict["name"] = self.name
        my_dict["path"] = self.path
        my_dict["user_id"] = self.user_id
        return my_dict
