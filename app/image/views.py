import simplejson
from flask import Blueprint, render_template, request, current_app, g

from .models import Image
from app.util.file_system import ImageFile

bp = Blueprint('gallery', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    images = ImageFile.all(current_app.config['GALLERY_ROOT_DIR'])
    return render_template(
        'gallery/gallery.html',
        title='Gallery',
        images=images
    )


@bp.route('/view/<filename>', methods=['GET', 'POST'])
def view(filename='', image_data=None):
    if filename:
        # Get image metadata
        image_data = g.session.query(Image).filter(Image.file_name == filename).first()
        image_data.viewed()     # update last seen and increment the image views
        g.session.add(image_data)

    return render_template(
        'gallery/view.html',
        image=filename,
        image_data=image_data
    )


@bp.route('/json')
def json():
    """Return a JSON containing an array of URL pointing to
    the images.
    """
    images = ImageFile.all(current_app.config['GALLERY_ROOT_DIR'])
    start = 0
    stop = len(images)

    try:
        if request.method == 'GET' and 'start' in request.args:
            start = int(request.args.get('start'))
        if request.method == 'GET' and 'stop' in request.args:
            stop = int(request.args.get('stop'))
    except ValueError:
        current_app.logger.debug(request)
        return "start/stop parameters must be numeric", 400

    images = images[start:stop]

    image_filenames = map(lambda x: x.filename, images)

    return simplejson.dumps(image_filenames)
