from database import db
class User(db.model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
