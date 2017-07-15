from flask import render_template, flash, redirect, url_for, request, g, Blueprint
from flask_login import login_user, logout_user, login_required

from app.models import User
from app.core import get_redirect_target
from app.forms import LoginForm
from app.database import db_session


bp = Blueprint('login', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():

    next = get_redirect_target()
    print('trying to login', next)
    form = LoginForm()

    if request.method == 'POST':
        print('checking authentication')
        if g.user and g.user.is_authenticated:
            pass
        elif form.validate_on_submit():
            email = form.login.data
            password = form.password.data
            remember = form.remember_me.data
            user = g.session.query(User).filter(User.email == email).first()

            if user:
                if user.verify_password(password):
                    # Not confident this is working as advertised
                    print('logging in remember me is', remember)
                    success = login_user(user, remember=remember)
                    flash('Login {s}.'.format(s='success!' if success else 'failed!'))

                    if next == url_for('login.login') and success:
                        next = ''

                    if not success:
                        flash('Invalid username or password.')
                else:
                    flash('Invalid username or password.')
            else:
                nickname = email.split('@')[0]
                nickname = User.make_unique_display_name(nickname)
                new_user = User(display_name=nickname, email=email, password=password)
                db_session.add(new_user)
                db_session.commit()
                flash('Successfully created login for', new_user.display_name)
            return redirect(next if next else url_for('gallery.index'))
    return render_template('login.html',
                           title='Sign In',
                           next=next,
                           form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged out.')
    return redirect(url_for('gallery.index'))
