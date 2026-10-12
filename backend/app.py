import firebase_admin

from firebase_admin import auth, credentials
from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
import requests

cred = credentials.RefreshToken('path/to/refreshToken.json')
default_app = firebase_admin.initialize_app(cred)


app = Flask(__name__)

db = SQLAlchemy(app)

app.secret_key = 'your-secret-key'

FIREBASE_API_KEY = ""

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

    firebase_auth_url = (f"https://googleapis.com{FIREBASE_API_KEY}")
    payload = {"email": data['email'], "password": data['password'], "returnSecureToken": True}

    try:
        response = requests.post(firebase_auth_url, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            session["user_id"] = response_data["localId"]
            return {'message': 'Login successful'}, 200

    except:
        return {'error': 'Invalid credentials'}, 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user_id", None)
    return {'message': 'User logged out'}, 200


if __name__ == '__main__':
    app.run()