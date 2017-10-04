from flask import render_template, current_app, Blueprint, request, g, redirect
from flask_login import login_required

from app.core import redirect_back, get_redirect_target
from app.gallery import Image

bp = Blueprint('upload', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    print('upload.index')
    next = get_redirect_target()
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']

        # Create image and metadata,resolve filename conflicts
        # Image inherits a filesystem object which is lost once the model is committed
        img = Image('', post=image, root=current_app.config['GALLERY_ROOT_DIR'])

        # Add this image to the users' record of images
        g.user.upload_image(img)

        # Add the uploaded images to the session
        g.session.add(g.user)

        return redirect_back('index.index')
    return render_template(
        'upload/upload.html',
        title='Upload',
        next=next
    )


@bp.route('/remove', methods=['GET', 'POST'])
def remove():
    next = get_redirect_target()
    print('hit remove')
    file = request.form.get('remove')
    print(file)
    if file:
        img = g.session.query(Image).filter(Image.file_name == file).first()
        print(img)
        # g.user.remove_image()
    return redirect(next if next else 'gallery.index')