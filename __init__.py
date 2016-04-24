import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from database import db

# from IPython import embed
import PCFG

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
#app.run()

from routes import webapp

app.register_blueprint(webapp)
