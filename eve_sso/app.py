from flask import Flask, render_template, redirect, request, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from preston.crest import Preston

from .models import db, User


# Create and configure app
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
# EVE CREST API connection
crest = Preston(
    user_agent='EVE SSO Python Stack example',
    client_id=app.config['EVE_OAUTH_CLIENT_ID'],
    client_secret=app.config['EVE_OAUTH_SECRET'],
    callback_url=app.config['EVE_OAUTH_CALLBACK']
)
# Database connection
db.app = app
db.init_app(app)
# User management
login_manager = LoginManager(app)
login_manager.login_message = ''
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """Return a User model object with the passed id.

    Args:
        user_id (str): user model id

    Returns:
        eve_sso.models.User: user with that id
    """
    return User.query.filter_by(id=int(user_id)).first()


@app.route('/')
@login_required
def index():
    """Show the index page for logged-in users.

    Args:
        None

    Returns:
        str: Rendered template 'index.html'
    """
    return render_template('index.html')


@app.route('/login')
def login():
    """Show a user the EVE SSO link so they can log in.

    Args:
        None

    Returns:
        str: Rendered template 'login.html'
    """
    return render_template('login.html', url=crest.get_authorize_url())


@app.route('/eve/callback')
def eve_oauth_callback():
    """Parse data back from the EVE SSO.

    This transient endpoint completes the EVE SSO login. Here, eve_sso.models.User
    objects are created for the user if they don't exist and the user is redirected
    to the index page.

    Args:
        None

    Returns:
        Redirect to the login endpoint if something failed or index endpoint
        if the login was successful
    """
    if 'error' in request.path:
        flash('There was an error in EVE\'s response', 'error')
        return url_for('login')
    try:
        auth = crest.authenticate(request.args['code'])
    except Exception as e:
        print('SSO callback exception: ' + str(e))
        flash('There was an authentication error signing you in.', 'error')
        return redirect(url_for('login'))
    character_info = auth.whoami()
    character_name = character_info['CharacterName']
    user = User.query.filter_by(name=character_name).first()
    if user:
        login_user(user)
        flash('Logged in', 'success')
        return redirect(url_for('index'))
    user = User(character_name)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    flash('Logged in', 'success')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Log the user out.

    Args:
        None

    Returns:
        Redirect to the login page
    """
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def error_404(e):
    """Catch 404 errors.

    Args:
        e (Exception): the exception from the server

    Returns:
        str: Rendered template 'error_404.html'
    """
    return render_template('error_404.html')


@app.errorhandler(500)
def error_500(e):
    """Catch 500 errors.

    Args:
        e (Exception): the exception from the server

    Returns:
        str: Rendered template 'error_500.html'
    """
    return render_template('error_500.html')
