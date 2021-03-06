"""Server package."""

from flask import Blueprint

server = Blueprint('server',
__name__, template_folder="templates")

from app.server.models import Server
from app.server import routes
