import os
import simplejson
from flask import Blueprint, render_template, request, current_app, send_file, g, abort

from app.models.file_system import ImageFile
from app.models.image import Image

bp = Blueprint('gallery', __name__)


@bp.route('/', methods=['GET', 'POST'])
def index():
    images = ImageFile.all(current_app.config['GALLERY_ROOT_DIR'])
    return render_template(
        'gallery.html',
        title='Gallery',
        images=images
    )


@bp.route('/view/<filename>', methods=['GET', 'POST'])
def imageview(filename='', image_data=None):
    if filename:
        # Get image metadata
        image_data = g.session.query(Image).filter(Image.file_name == filename).first()
        image_data.viewed()     # update last seen and increment the image views
        g.session.add(image_data)

    return render_template(
        'image.html',
        image=filename,
        image_data=image_data
    )


@bp.route('/image/<filename>', methods=['GET'])
def image(filename=''):
    file_path = os.path.join(current_app.config['GALLERY_ROOT_DIR'], filename)
    file_exists = os.path.isfile(file_path)
    return send_file(file_path) if file_exists else abort(400)


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
