import datetime
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from selenium import webdriver

import subscribely.modo as modo
import subscribely.spiders.spotify as spotify

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'subscribely.db'),
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
#    modo._set_connection(db)
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
    cur = db.execute('SELECT * FROM user_subscriptions '
        'INNER JOIN services ON user_subscriptions.service_id = services.service_id '
        'INNER JOIN user_modo ON user_subscriptions.user_id = user_modo.user_id')
    subscriptions = cur.fetchall()
    current_datetime = datetime.datetime.now()
    current_time = '-'.join(map(str, [current_datetime.year, current_datetime.month, current_datetime.day]))
    print(subscriptions)
    return render_template('dashboard.html', subscriptions=subscriptions, current_date=current_time)


@app.route('/subscriptions/<id>/enable', methods=['GET'])
def enable_subscription(id):
    db = get_db()
    cursor = db.execute('select user_id, service_id, is_active from user_subscriptions where subscription_id = ?', (id,))
    subscription = cursor.fetchone()
    user_id = subscription[0]
    service_id = subscription[1]
    is_active = subscription[2]

    if (is_active):
        return

    result = False

    """
    gift_card_status = spotify.gift_card_status()
    if (gift_card_status):
        cursor.execute('UPDATE user_subscriptions SET is_active=? WHERE subscription_id=?', (True, id))
        get_db().commit()
    else:
        #TODO: code = from modo
        result = spotify.enter_gift_card_code(code)
    """

    data = modo.process_payment_virtual_cc(get_db(), user_id, service_id)
    result = spotify.subscribe_with_credit_card_info(data['pan'], data['exp_month'], data['exp_year'], data['cvv'], '78787')

    if (result):
        flash('Subscription successfully enabled.')
        cursor.execute('UPDATE user_subscriptions SET is_active=? WHERE subscription_id=?', (True, id))
        get_db().commit()
    else:
        flash('Sorry, something went wrong!')

    return redirect(url_for('dashboard'))

@app.route('/subscriptions/<id>/disable', methods=['GET'])
def disable_subscription(id):
    db = get_db()
    cursor = db.execute('select is_active from user_subscriptions where subscription_id = ?', (id,))
    subscription = cursor.fetchone()
    is_active = subscription[0]

    if not is_active:
        return

    cursor.execute('UPDATE user_subscriptions SET is_active=? WHERE subscription_id=?', (False, id))
    get_db().commit()

    flash('Subscription successfully disabled.')
    return redirect(url_for('dashboard'))


@app.route('/payment_methods', methods=['GET', 'POST'])
def payment_methods():
    error = None
    if request.method == 'POST':
        modo.add_credit_card(
            connection=get_db(),
            user_id=1,
            name_on_card=request.form['name_on_card'],
            credit_card_number=request.form['credit_card_number'],
            expiration_month=int(request.form['expiration_month']),
            expiration_year=int(request.form['expiration_year']),
            security_code=int(request.form['security_code']),
            billing_address=request.form['billing_address'],
            zip_code=request.form['zip_code'],
        )
        print(request.form['credit_card_number'])
    return render_template('account-info.html', error=error)

@app.route('/update_credentials', methods=['GET', 'POST'])
def update_credentials():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = get_db()
        cursor = get_db().cursor()
        cursor.execute('UPDATE user_subscriptions SET username=?, password=? WHERE user_id=1 AND service_id=1',
            (request.form['username'], request.form['password']))
        connection.commit()
    return render_template('update_credentials.html', error=error)

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
