from datetime import datetime

from apps import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False, unique=True)
    answer = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return str(self.question)


if __name__ == "__main__":
    db.create_all()
