import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from selenium import webdriver

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
    cur = db.execute('select * from user_subscriptions '
        'inner join services on user_subscriptions.service_id = services.service_id '
        'inner join user_modo on user_subscriptions.user_id = user_modo.user_id')
    subscriptions = cur.fetchall()
    print(subscriptions)
    return render_template('dashboard.html', subscriptions=subscriptions)


@app.route('/subscriptions/<id>/enable', methods=['POST'])
def enable_subscription(id):
    db = get_db()
    cursor = db.execute('select * from user_subscriptions where subscription_id = ?', (id,))
    subscription = cursor.fetchone()

    if (subscription.is_active):
        return

    result = False
    gift_card_status = gift_card_status()
    if (gift_card_status):
        cursor.execute('UPDATE user_subscription SET is_active=? WHERE subscription_id=?', (True, id))
        connection.commit()
    else:
        #TODO: code = from modo
        result = enter_gift_card_code(code)

    if (result):
        flash('Subscription successfully enabled.')
    else:
        flash('Sorry, something went wrong!')

    return redirect(url_for('dashboard'))

@app.route('/subscriptions/<id>/disable', methods=['POST'])
def disable_subscription(id):
    db = get_db()
    cursor = db.execute('select * from user_subscriptions where subscription_id = ?', (id,))
    subscription = cursor.fetchone()

    if (!subscription):
        return

    cursor.execute('UPDATE user_subscription SET is_active=? WHERE subscription_id=?', (False, id))
            connection.commit()

    flash('Subscription successfully disabled.')
    return redirect(url_for('dashboard'))


@app.route('/payment_methods', methods=['GET', 'POST'])
def payment_methods():
    error = None
        if request.method == 'POST':
            print(request.form['payinfo'])
        elif request.method == 'GET':
            print('Current available payment goes here.')
    return render_template('login.html', error=error)

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

def gift_card_status():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    driver.get("https://accounts.spotify.com/en-US/login")
    driver.find_element_by_id("login-username").send_keys("ktperryfan007")
    driver.find_element_by_id("login-password").send_keys("tswifty")

    login_button = driver.find_element_by_css_selector("button")
    login_button.click()

    success_notification = driver.find_element_by_xpath("//*[contains(text(), 'You are logged in as ktperryfan007.')]")
    print(success_notification.text)

    driver.get("https://www.spotify.com/us/account/subscription/")

    gift_card_status = None
    prepaid_notifications = driver.find_elements_by_xpath("//p[contains(text(), 'Your pre-paid Premium will end on')]")
    nonrecurring_dates = driver.find_elements_by_xpath("//b[@class='nonrecurring-date']")
    if (len(prepaid_notifications) == 1):
        print("gift card is active until " + nonrecurring_dates[0].text)
        gift_card_status = nonrecurring_dates[0].text
    else:
        print("no active gift card found")

    driver.quit()

    return gift_card_status

def enter_gift_card_code(code):
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    driver.get("https://accounts.spotify.com/en-US/login")
    driver.find_element_by_id("login-username").send_keys("ktperryfan007")
    driver.find_element_by_id("login-password").send_keys("tswifty")

    login_button = driver.find_element_by_css_selector("button")
    login_button.click()

    success_notification = driver.find_element_by_xpath("//*[contains(text(), 'You are logged in as ktperryfan007.')]")
    print(success_notification.text)

    driver.get("https://www.spotify.com/us/redeem/prepaid/")

    driver.find_element_by_id("redeem_code_token").send_keys(code)
    enter_code_button = driver.find_element_by_id("redeem_code_submit")
    enter_code_button.click()

    invalid_notifications = driver.find_elements_by_xpath("//p[contains(text(), 'Unfortunately this Premium code does not seem to be valid')]")
    driver.quit()

    if (len(invalid_notifications) > 0):
        return False

    return True