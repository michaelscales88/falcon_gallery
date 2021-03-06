"""
Consumes a posted file, creates metadata and creates the file.
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
        """Get a POST file and save it to the user.UPLOAD_DIR"""
        full_path = os.path.join(self.root_dir, self.filename)

        # Handle name conflicts
        if os.path.isfile(full_path):
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
            self.filename = '{0}({1}){2}'.format(file, counter, ext)    # Update filename post collision resolution
            full_path = os.path.join(
                current_app.config['UPLOAD_DIR'],
                self.filename
            )  # Save to the upload directory

        post.save(full_path)

    @classmethod
    def all(cls, root):
        """
        Return a list of files contained in the directory pointed by user.GALLERY_ROOT_DIR.
        Ignores files without the correct extension
        """
        return [cls(x, root=root) for x in os.listdir(root) if cls.allowed_extension(x)]

    @staticmethod
    def allowed_extension(file, extensions=None):
        return file.endswith(extensions if extensions else current_app.config['ALLOWED_EXTENSIONS'])


class ImageFile(FilesystemObject):
    pass
