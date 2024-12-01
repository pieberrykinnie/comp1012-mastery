from datetime import datetime
from . import db, Problem


class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey(
        'problem.id'), nullable=False)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    solved = db.Column(db.Boolean, nullable=False, default=False)
    last_attempt = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    # Add relationship
    problem = db.relationship("Problem", backref="progress")

    __table_args__ = (
        db.UniqueConstraint('user_id', 'problem_id',
                            name='unique_user_problem'),
    )
