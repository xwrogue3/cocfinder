from contextlib import closing
from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_path='/static')
app.config.from_envvar('COCFINDER_SETTINGS')

db = SQLAlchemy(app)

from cocfinder import models, views

