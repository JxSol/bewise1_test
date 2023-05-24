from typing import NoReturn

import requests
from flask import jsonify, request, Response
from requests import RequestException
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import InternalServerError

from . import blueprint
from .models import Question
from apps import db


def valid_positive_integer(value: int) -> bool:
    """Check if value is a positive integer."""
    if value > 0:
        return True
    raise ValueError('Value is not a positive integer.')


def get_questions_from_api(count: int) -> Response | NoReturn:
    """Get data from jService."""
    url = f"https://jservice.io/api/random?count={count}"
    response = requests.get(url)

    if response.status_code == 200:
        questions = response.json()
        return jsonify(questions)
    else:
        raise RequestException('Failed to get data from jService.')


@blueprint.route('/quiz', methods=['POST'])
def create_questions() -> Response | NoReturn:
    """Create questions."""
    questions_num = request.get_json().get('questions_num')

    # Get questions from API
    try:
        valid_positive_integer(questions_num)
        response = get_questions_from_api(questions_num)
    except (RequestException, ValueError) as e:
        raise InternalServerError(e.message)

    # Save questions to database
    errors = 0
    for data in response.json:
        question = Question(
            question=data.get('question'),
            answer=data.get('answer'),
        )
        try:
            db.session.add(question)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            errors += 1

    # Get more questions if it needed and return latest
    if errors > 0:
        return create_questions(str(errors))

    # Return latest question
    latest = Question.query.order_by(Question.created.desc()).first()
    if latest:
        return jsonify(latest.serialize())
    return jsonify({})
