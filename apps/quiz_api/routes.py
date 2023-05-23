from flask import render_template
from . import blueprint


@blueprint.route('/')
def hello_world():
    return render_template('quiz/quiz.html')
