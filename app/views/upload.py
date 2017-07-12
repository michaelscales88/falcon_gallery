from flask import render_template, current_app, Blueprint, request, flash, g
from flask_login import login_required
from app.models.file_system import Image
from app.models.image import Image as ImageModel
from app.core import redirect_back, get_redirect_target


bp = Blueprint('upload', __name__)  # , template_folder='templates'


@bp.route('/upload', methods=['GET', 'POST',])
@login_required
def index():
    next = get_redirect_target()
    if request.method == 'POST' and 'image' in request.files:
        image = request.files['image']
        img = Image('', post=image, root=current_app.config['GALLERY_ROOT_DIR'])
        g.session.add(ImageModel(file_name=img.filename, name=img.filename.split('.')[0]))  # Default: filename sans ext
        g.session.commit()
        flash('Added image', img.filename)
        return redirect_back('index.index')
    return render_template(
        'upload.html',
        title='Upload',
        next=next
    )
