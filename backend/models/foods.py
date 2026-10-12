from database import db
class Food(db.model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
