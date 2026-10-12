from database import db
class Exercise(db.model):
    __tablename__ = "exercises"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    muscle_group = db.Column(db.String(100))
    description = db.Column(db.Text)