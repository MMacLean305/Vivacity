from database import db
from datetime import datetime, timezone
class ExerciseLog(db.Model):
    __tablename__ = "exercise_logs"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    date = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))