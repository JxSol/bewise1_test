from flask import Blueprint

blueprint = Blueprint(
    'quiz_blueprint',
    __name__,
    url_prefix='/api',
)
