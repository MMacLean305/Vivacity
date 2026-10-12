import firebase_admin

from firebase_admin import auth, credentials
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from models import Exercise, Food, User
import requests
import os

from dotenv import load_dotenv

load_dotenv()

cred = credentials.Certificate('serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')

@app.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    try:
        user = auth.create_user(email=data['email'], password=data['password'])
        return {'uid': user.uid}, 201
    except:
        return {'error': 'User already exists'}, 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    firebase_auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": data['email'], "password": data['password'], "returnSecureToken": True}

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


if __name__ == '__main__':
    app.run()