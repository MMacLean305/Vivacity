import firebase_admin

from firebase_admin import auth, credentials
from flask import Flask, render_template, request, session
from database import db
from models import Exercise, Food, User, SessionLog, ExerciseLog, FoodLog
import requests
import os

from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate('serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)


app = Flask(
    __name__,
    template_folder = "../frontend/templates",
    static_folder = "../frontend/static",
    )
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vivacity.db'
db.init_app(app)

with app.app_context():
    db.create_all()

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    try:
        firebase_user = auth.create_user(email=data['email'], password=data['password'])
        user = User(firebase_uid = firebase_user.uid, username = data['username'], email=data['email'], role = 'member')
        db.session.add(user)
        db.session.commit()
        return {'uid': firebase_user.uid}, 201
    except Exception as e:
        db.session.rollback()

        if 'firebase_user' in locals():
            auth.delete_user(firebase_user.uid)
        
        print('Registration Error: ', e)
        return{'error' : 'Registration failed'}, 400

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()

    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return {'error': 'Invalid username or password'}, 404

    firebase_auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": user.email, "password": data['password'], "returnSecureToken": True}

    try:
        response = requests.post(firebase_auth_url, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            session["user_id"] = response_data["localId"]
            return {'message': 'Login successful'}, 200
        else:
            return {'error': 'Login failed'}, 401

    except:
        return {'error': 'Invalid credentials'}, 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user_id", None)
    return {'message': 'User logged out'}, 200

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route('/api/exercises', methods = ['GET'])
def get_exercises():
    input_ = request.args.get('search', '')
    exercises = Exercise.query.filter(Exercise.name.ilike(f"%{input_}%")).all()

    res = []
    for e in exercises:
        res.append({
            "id": e.id, "name" : e.name, 'muscle_group': e.muscle_group, "description": e.description})
    return res, 200

#Should probably add some safety checks!!!!!!
@app.route("/api/sessions", methods = ["POST"])
def make_session():
    firebase_uid = session.get('user_id')
    user = User.query.filter_by(firebase_uid = firebase_uid).first()
    new_session = SessionLog(user_id = user.id)
    db.session.add(new_session)
    db.session.commit()
    return {'session_id': new_session.id}, 201

if __name__ == '__main__':
    app.run()