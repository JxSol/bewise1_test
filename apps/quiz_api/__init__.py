from flask import Blueprint
from . import models

blueprint = Blueprint(
    'quiz_blueprint',
    __name__,
    url_prefix='/api',
)
