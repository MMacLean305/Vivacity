from database import db
from datetime import datetime, timezone
class FoodLog(db.Model):
    __tablename__ = "food_logs"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'))
    quantity = db.Column(db.Float)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))