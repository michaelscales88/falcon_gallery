from datetime import datetime

from flask import render_template, redirect, request, g, current_app, flash
from flask_login import login_required, current_user

from app import app, lm, si
from app.models import User
from app.core import get_redirect_target, transfer_uploads
from app.database import db_session


@app.before_request
def before_request():
    print('setup')
    g.user = current_user
    g.session = db_session
    g.search_enabled = current_app.config['ENABLE_SEARCH']
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
    if g.search_enabled:
        si.register_class(User)  # update whoosh with User information


@app.teardown_request
def teardown(error):
    print('teardown')
    session = getattr(g, 'session', None)
    # Only commit if we get this far
    if session:
        session.commit()

    # Good spot to offer a "review" option Y: do stuff then transfer N: transfer
    transfer_uploads()  # This EOL for my file object "session"
    flash('Uploaded images!')


@app.teardown_appcontext
def shutdown_session(exception=None):
    print('absolute session end')
    db_session.remove()     # Be certain than the session closes


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db_session.rollback()
    return render_template('500.html'), 500


@app.route('/splash', methods=['GET', 'POST'])
def splash():
    next = get_redirect_target()
    clicked = request.form.get('clicked')
    if clicked:
        return redirect(next)
    else:
        pass
        # Show recent items for the user
    return render_template(
        'splash.html',
        title='Recent',
        next=next
    )


@app.route("/settings")
@login_required
def settings():
    pass


@lm.user_loader
def load_user(id):
    return User.get(id=int(id))
