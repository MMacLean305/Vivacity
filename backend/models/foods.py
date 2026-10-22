from database import db
class Food(db.Model):
    __tablename__ = "foods"
    id = db.Column(db.Integer, primary_key=True)
    fdcId = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    fats = db.Column(db.Float)
    carbs = db.Column(db.Float)
    protein = db.Column(db.Float)