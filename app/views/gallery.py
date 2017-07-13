from flask import Blueprint, render_template, request, current_app, send_file, g
from sqlalchemy.sql import expression
import simplejson
from app.models import Image
from app.models.image import Image as ImageModel
import os


bp = Blueprint('gallery', __name__)    # , static_folder='static' , template_folder='templates'


@bp.route('/', methods=['GET', 'POST', ])
def index():
    images = Image.all(current_app.config['GALLERY_ROOT_DIR'])
    image_list = [f.filename for f in images]
    image_data = g.session.query(ImageModel).filter(ImageModel.file_name.in_(image_list)).all()   # Query ImageModel table
    return render_template(
        'index.html',
        title='Gallery',
        images=images,
        image_data=image_data
    )


@bp.route('/alternate', methods=['GET', 'POST'])
def imageview(filename=''):
    return render_template(
        'index.html'
    )


@bp.route('/image/<filename>', methods=['GET'])
def image(filename=''):
    return send_file(os.path.join(current_app.config['GALLERY_ROOT_DIR'], filename))


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
