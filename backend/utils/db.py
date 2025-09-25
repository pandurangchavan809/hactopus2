import sqlite3
from flask import Flask, g
from flask_cors import CORS
import os

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'complaints.db')

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        with open(os.path.join(os.path.dirname(__file__), '..', 'schema.sql'), 'r') as f:
            conn.executescript(f.read())

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.teardown_appcontext(close_connection)
    with app.app_context():
        init_db()
    return app
