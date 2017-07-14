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
            return redirect(url_for('gallery.index'))

        if form.validate_on_submit():
            user_email = str(form.login.data)
            password = str(form.password.data)
            remember = form.remember_me.data
            user = User.query.filter_by(email=user_email).first()

            if user:
                if user.verify_password(password):
                    # Not confident this is working as advertised
                    print('logging in remember me is', remember)
                    login_user(user, remember=remember)
                    flash('Logged in successfully.')
                else:
                    flash('Invalid login')
                    print('set next', next)
            else:
                nickname = user_email.split('@')[0]
                nickname = User.make_unique_display_name(nickname)
                new_user = User(display_name=nickname, email=user_email, password=password)
                db_session.add(new_user)
                db_session.commit()
                flash('Successfully created login for', new_user.display_name)
        print('redirecting', next)
        return redirect(next if next else 'gallery.index')
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

