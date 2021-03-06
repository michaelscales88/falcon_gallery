import os
from flask import request, url_for, abort, redirect, current_app, send_file
from urllib.parse import urlparse, urljoin
from shutil import move


def send_or_404(directory, file):
    file_path = os.path.join(directory, file)
    file_exists = os.path.isfile(file_path)
    return send_file(file_path) if file_exists else abort(400)


def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
        else:
            return abort(400)


def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ('http', 'https')
        and ref_url.netloc == test_url.netloc
    )


def transfer_uploads():
    uploads = os.listdir(current_app.config['UPLOAD_DIR'])
    for upload in uploads:
        move(
            os.path.join(current_app.config['UPLOAD_DIR'], upload),     # SRC
            os.path.join(current_app.config['GALLERY_ROOT_DIR'], upload)    # DESTINATION
        )
