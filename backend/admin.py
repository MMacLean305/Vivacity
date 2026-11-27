import sys
from app import app
from database import db
from models import User

with app.app_context():
    user = User.query.filter_by(username = sys.argv[1]).first()
    if user is None:
        print("No user named", sys.argv[1])
    else:
        user.role = "admin"
        db.session.commit()
        print(user.username, "is now an admin")