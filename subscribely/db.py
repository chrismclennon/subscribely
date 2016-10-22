import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'subscribely.db'),
    SECRET_KEY='pQS5Aby1A2jSnSbYKu3mbNIl53NoN6hoPw1C1F7WIgOESsufjpYf6obXRHJlhjsp43NhDyG79GlRykMYOacC0f3qJoM2ssGWTK9H',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
