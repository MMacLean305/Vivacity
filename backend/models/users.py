from database import db
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    firebase_uid = db.Column(db.String(128), unique = True, nullable = False)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(255), unique = True)
    role = db.Column(db.String(20), default = "member", nullable = False)
