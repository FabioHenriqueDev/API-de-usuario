from  flask import Flask
from flask_sqlalchemy import SQLAlchemy
from extensions import db, jwt
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import re
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import secrets

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app) 
CORS(app)
jwt.init_app(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

bcrypt = Bcrypt(app)

from models import Usuario, CodigoVerificacao

with app.app_context():
    
    db.create_all()


    
import routes