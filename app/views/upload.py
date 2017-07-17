from flask import render_template, current_app, Blueprint, request, g
from flask_login import login_required

from app.core import redirect_back, get_redirect_target
from app.models.image import Image

bp = Blueprint('upload', __name__)


@bp.route('/upload', methods=['GET', 'POST',])
@login_required
def index():
    next = get_redirect_target()
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']

        # Create image and metadata,resolve filename conflicts
        # Image inherits a filesystem object which is lost once the model is committed
        img = Image('', post=image, root=current_app.config['GALLERY_ROOT_DIR'])

        # Add this image to the users' record of images
        g.user.upload(img)

        # Add the uploaded images to the session
        g.session.add(g.user)

        return redirect_back('index.index')
    return render_template(
        'upload.html',
        title='Upload',
        next=next
    )
