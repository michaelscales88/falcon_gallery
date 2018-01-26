from flask import render_template, flash, redirect, url_for, request, g, Blueprint
from flask_login import login_user, logout_user, login_required

from .core import new_user, existing_user
from app.core import get_redirect_target


bp = Blueprint(
    'user',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/user/static'
)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():

    if not any((g.user, g.user.is_authenticated)):
        return redirect(
            url_for('index')
        )

    return render_template(
        'settings_template.html',
        title='Settings',
        user=g.user
    )


@bp.route('/login', methods=['GET', 'POST'])
def login():

    if all((g.user, g.user.is_authenticated)):
        return redirect(
            url_for('index')
        )

    next_tgt = get_redirect_target()

    # Parser section
    g.parser.add_argument('user_name', type=str, location='form')
    g.parser.add_argument('password', type=str, location='form')
    g.parser.add_argument('remember_me', type=bool, location='form')
    args = g.parser.parse_args()

    if request.method == 'POST':

        user = existing_user(g.session, args)

        if not user:
            user = new_user(args)
            g.session.add(user)
            g.session.commit()
            flash('Successfully created login for', user.alias)

        if user.verify_password(args['password']):
            # User Login
            success = login_user(user, remember=args['remember_me'])
            flash('Login {s}.'.format(s='success!' if success else 'failed!'))

        return redirect(next_tgt)

    return render_template(
        'login_template.html',
        title='Sign In',
        next=next_tgt
    )


@bp.route("/logout", methods=['GET'])
@login_required
def logout():
    success = logout_user()
    flash('Logout {s}.'.format(s='success!' if success else 'failed!'))
    return redirect(url_for('index'))
