from flask import render_template, current_app, Blueprint, request, g
from flask_login import login_required

from app.core import redirect_back, get_redirect_target
from app.image import Link, Image

bp = Blueprint('user', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    next = get_redirect_target()
    user = g.user
    if not user:
        redirect_back('gallery.index')

    if request.method == 'POST':
        # request parsing
        print(request.form)
        edit = request.form.get('edit')
        remove = request.form.get('remove')
        image = request.files.get('user_image')

        if image:
            print('adding image', dir(image))
            img = Image('', post=image, root=current_app.config['AVATAR_DIR'])
            user.avatar = img.file_name
            g.session.add(user)
        if edit:
            pass
            # link = g.session.query(Link).filter(Link.link == edit).first()
            # link.link = edit
            # g.session.add(link)
        if remove:
            link = g.session.query(Link).filter(Link.link == remove).first()
            user.remove_link(link)
        else:
            link_type = request.form.get('link_type')
            link = request.form.get('link_proper')
            if link and link_type:
                user.add_link(Link(link=link, link_type=link_type))

        # Put all the changes to our user in the session
        g.session.add(user)

    return render_template(
        'user/settings.html',
        title='Settings',
        next=next,
        user=user
    )
