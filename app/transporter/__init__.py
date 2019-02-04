# app/admin/__init__.py

from flask import Blueprint

transporter = Blueprint('transporter', __name__)

from . import views
