from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    week = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    test_cases = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
