import os
import csv
from app import app
from database import db
from models import Exercise

csv_file = os.path.join(os.path.dirname(__file__), "data", "exercises.csv")

with app.app_context():
    with open(csv_file, newline = '', encoding = 'utf-8-sig') as file:
        reader = csv.DictReader(file)
        for r in reader:
            seen = Exercise.query.filter_by(name = r["name"]).first()
            if seen is None:
                exercise = Exercise(name = r["name"], muscle_group = r["muscle_group"], description = r["description"])
                db.session.add(exercise)

    db.session.commit()
    print("Import complete")