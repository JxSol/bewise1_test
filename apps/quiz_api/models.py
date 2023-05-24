from datetime import datetime

from apps import db


class Question(db.Model):
    """Question model.
    Attrs:
        id (Integer): identifier
        question (String): text of the question
        answer (String): text of the answer
        created (DateTime): time when the record was created
    """
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False, unique=True)
    answer = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)

    def serialize(self) -> dict:
        """Serialize the object."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return str(self.question)


if __name__ == "__main__":
    db.create_all()
