from database import db
from datetime import datetime, timezone
class SessionLog(db.Model):
    __tablename__ = "session_log"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))