import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='uoOBAh6F4yKJQXXQgjLSYy8bxuyri58F',
    USERNAME='kperry@yomail.com',
    PASSWORD='tswifty'
))
app.config.from_envvar('SUBSCRIBELY_SETTINGS', silent=True)

# DATABASE
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# ROUTING
@app.route('/')
def dashboard():
    db = get_db()
    cur = db.execute('select * from services')
    subscriptions = cur.fetchall()
    return render_template('dashboard.html', subscriptions=subscriptions)

@app.route('/subscriptions/<id>/enable', methods=['POST'])
def enable_subscription():
    # TODO: authenticate and enable subscription
    flash('Subscription successfully enabled.')
    return redirect(url_for('dashboard'))

@app.route('/subscriptions/<id>/disable', methods=['POST'])
def disable_subscription():
    # TODO: authenticate and disable subscription
    flash('Subscription successfully disabled.')
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            print('success')
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('dashboard'))
