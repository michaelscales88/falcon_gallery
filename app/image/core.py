from flask import current_app
from app.core import send_or_404


def image(filename=''):
    return send_or_404(current_app.config['GALLERY_ROOT_DIR'], filename)
