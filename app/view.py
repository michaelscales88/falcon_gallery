from datetime import datetime

from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import login_user, logout_user, login_required, current_user

from app import app, lm, si
from app.models import User
from app.core import get_redirect_target, redirect_back, transfer_uploads
from app.forms import LoginForm
from app.database import db_session


@app.before_request
def before_request():
    print('setup')
    g.user = current_user
    g.session = db_session
    g.search_enabled = current_app.config['ENABLE_SEARCH']
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db_session.add(g.user)
        db_session.commit()
        g.report_date = datetime.today().date()
    if g.search_enabled:
        si.register_class(User)  # update whoosh with User information
        # g.search_form = SearchForm()


@app.teardown_request
def teardown(error):
    transfer_uploads()  # This EOL for my file object "session"
    print('teardown')


@app.teardown_appcontext
def shutdown_session(exception=None):
    print('closing session', db_session)
    db_session.remove()     # Be certain than the session closes


@app.errorhandler(404)
def not_found_error(error):
    print('found a 404')
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    print('found a 500')
    db_session.rollback()
    return render_template('500.html'), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    print('trying to login')
    next = get_redirect_target()
    form = LoginForm()

    if request.method == 'POST':

        if g.user is not None and g.user.is_authenticated:
            return redirect(url_for('gallery.index'))

        if form.validate_on_submit():
            user_email = str(form.login.data)
            user = User.query.filter_by(email=user_email).first()

            if not user:
                nickname = user_email.split('@')[0]
                nickname = User.make_unique_nickname(nickname)
                user = User(nickname=nickname, email=user_email)
                db_session.add(user)
                db_session.commit()

            # remember_me = False
            # if 'remember_me' in g.session:
            #     remember_me = g.session['remember_me']
            #     g.session.pop('remember_me', None)
            # login_user(user, remember=remember_me)
            login_user(user)
            flash('Logged in successfully.')
            return redirect_back('gallery.index')
    return render_template('login.html',
                           title='Sign In',
                           next=next,
                           form=form)


@app.route("/settings")
@login_required
def settings():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('gallery.index'))


@lm.user_loader
def load_user(id):
    return User.get(id=int(id))
