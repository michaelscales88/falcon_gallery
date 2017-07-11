from flask import Blueprint, render_template, request, current_app
import simplejson
from app.models import Image


bp = Blueprint('gallery', __name__)    # , static_folder='static' , template_folder='templates'


@bp.route('/', methods=['GET', 'POST', ])
def index():
    images = Image.all(current_app.config['GALLERY_ROOT_DIR'])
    print('gallery.index')
    return render_template(
        'index.html',
        title='Gallery',
        images=images
    )


@bp.route('/json')
def json():
    """Return a JSON containing an array of URL pointing to
    the images.
    """
    images = Image.all(current_app.config['GALLERY_ROOT_DIR'])
    start = 0
    stop = len(images)

    try:
        if request.method == 'GET' and 'start' in request.args:
            start = int(request.args.get('start'))
        if request.method == 'GET' and 'stop' in request.args:
            stop = int(request.args.get('stop'))
    except ValueError:
        current_app.logger.debug(request)
        return ("start/stop parameters must be numeric", 400)

    images = images[start:stop]

    image_filenames = map(lambda x: x.filename, images)

    return simplejson.dumps(image_filenames)
