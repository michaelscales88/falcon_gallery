"""
This module aims to create a model having the filesystem as backend, since
if someone don't want to add extra metadata more than the metadata given
by the file informations is useless to use a database.

TODO: traverse directory.
"""
from werkzeug.utils import secure_filename
from flask import current_app

import os


class FilesystemObjectDoesNotExist(Exception):
    pass


class FilesystemObject(object):
    def __init__(self, filename, post=None, root=None):
        """Create an object from the information of the given filename or from a
        uploaded file.

        Example of usage:

            if request.method == 'POST' and 'photo' in request.POST:
                f = FilesystemObject('cats.png', request.POST['photo'])

        """
        self.root_dir = root
        self.filename = filename if not post else secure_filename(post.filename)
        self.abspath = os.path.join(self.root_dir, filename)

        if post:
            self.upload(post)

        try:
            stats = os.stat(self.abspath)
        except IOError as e:
            raise FilesystemObjectDoesNotExist(e)

        self.timestamp = stats.st_mtime

    def upload(self, post):
        """Get a POST file and save it to the settings.GALLERY_ROOT_DIR"""
        # http://flask.pocoo.org/docs/patterns/fileuploads/
        file_name = os.path.join(self.root_dir, self.filename)

        # Handle name conflicts
        if os.path.isfile(file_name):
            file, ext = os.path.splitext(self.filename)
            counter = 1

            # Test filename collision in gallery directory not uploads
            while os.path.isfile(
                    os.path.join(
                        self.root_dir,
                        '{0}({1}){2}'.format(file, counter, ext)
                    )
            ):
                counter += 1

            file_name = os.path.join(
                current_app.config['UPLOAD_DIR'],
                '{0}({1}){2}'.format(file, counter, ext)
            )  # Save to the upload directory

        post.save(file_name)

    @classmethod
    def all(cls, root):
        """
        Return a list of files contained in the directory pointed by settings.GALLERY_ROOT_DIR.
        Ignores files without the correct extension
        """
        return [cls(x, root=root) for x in os.listdir(root) if cls.allowed_extension(x)]

    @staticmethod
    def allowed_extension(file, extensions=None):
        return file.endswith(extensions if extensions else current_app.config['ALLOWED_EXTENSIONS'])


class Image(FilesystemObject):
    pass
