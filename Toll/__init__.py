from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from googlemaps import Client
load_dotenv()
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///toll.db')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY") or os.urandom(24).hex()
try:
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if api_key and api_key != "your_actual_api_key_here":
        gmaps = Client(key=api_key)
    else:
        gmaps = None
except Exception:
    gmaps = None
db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from Toll import routes
with app.app_context():
    db.create_all()