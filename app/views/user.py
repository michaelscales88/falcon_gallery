from flask import render_template, current_app, Blueprint, request, g
from flask_login import login_required

from app.core import redirect_back, get_redirect_target
from app.models import Link

bp = Blueprint('user', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    next = get_redirect_target()
    user = g.user
    if not user:
        redirect_back('gallery.index')

    # request parsing
    link_type = request.form.get('link_type')
    link = request.form.get('link_proper')

    # logic
    print(link_type, link)
    g.user.links.append(Link(link=link, link_type=link_type))

    # Put all the changes to our user in the session
    g.session.add(g.user)

    return render_template(
        'user/settings.html',
        title='Settings',
        next=next,
        user=user
    )
