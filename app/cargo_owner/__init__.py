# app/admin/__init__.py

from flask import Blueprint

cargo_owner = Blueprint('cargo_owner', __name__)

from . import views
