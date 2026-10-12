import firebase_admin

from firebase_admin import auth, credentials
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

cred = credentials.RefreshToken('path/to/refreshToken.json')
default_app = firebase_admin.initialize_app(cred)

app = Flask(__name__)

db = SQLAlchemy(app)

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
    try:
        user = auth.get_user_by_email(email=data['email'])
        if auth.verify_password(password=data['password'], user=user):
            return {'uid': user.uid}, 200
        else:
            return {'error': 'Invalid credentials'}, 401
    except:
        return {'error': 'User not found'}, 404

@app.route('/logout', methods=['POST'])
def logout():
    pass


if __name__ == '__main__':
    app.run()