from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(100), nullable=False)
    attendance = db.Column(db.Float, nullable=False)
    tasks = db.Column(db.Float, nullable=False)
    teamwork = db.Column(db.Float, nullable=False)
    deadlines = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(50), nullable=False)
    explanation = db.Column(db.Text, nullable=False)  # Stores explanation
    suggestion = db.Column(db.String(255), nullable=False)  # New: Stores suggestion
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
