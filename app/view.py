from datetime import datetime

from flask import render_template, redirect, request, g, current_app, flash, url_for
from flask_login import current_user
from flask_restful.reqparse import RequestParser

from app import app, si
from app.core import get_redirect_target, transfer_uploads, send_or_404
from app.database import db_session
from app.image.models import Image
from app.user import User


@app.route('/')
def catch_all():
    return redirect(
        url_for('image.gallery')
    )


@app.before_request
def before_request():
    print('setup')
    g.user = current_user
    g.session = db_session
    g.search_enabled = current_app.config['ENABLE_SEARCH']
    g.parser = RequestParser()
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
    if g.search_enabled:
        si.register_class(User)  # update whoosh
        si.register_class(Image)


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


@app.route('/showcase', methods=['GET', 'POST'])
def showcase():
    next = get_redirect_target()
    clicked = request.form.get('clicked')
    if clicked:
        return redirect(next)
    else:
        pass
        # Show bitching splash page stuff

    return render_template(
        'showcase.html',
        title='Recent',
        next=next
    )


@app.route('/avatar/<filename>', methods=['GET'])
def avatar(filename=''):
    return send_or_404(current_app.config['AVATAR_DIR'], filename)
