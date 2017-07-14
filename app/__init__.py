from flask import Flask, Blueprint, url_for
from flask_restful import Api
from flask_login import LoginManager
import os
import shutil


# store private information in instance
app = Flask(__name__, instance_relative_config=True, template_folder='templates', static_folder='static')

# Load default settings
app.config.from_object('app.default_config.DevelopmentConfig')

# Start the index service
if app.config['ENABLE_SEARCH']:
    from whooshalchemy import IndexService
    si = IndexService(config=app.config)
    if os.path.isdir(app.config['WHOOSH_BASE']):
        shutil.rmtree(app.config['WHOOSH_BASE'])  # fresh index from whoosh prevents errors/slowdowns


# Avoid favicon 404
@app.route("/favicon.ico")
def favicon():
    return url_for('static', filename='favicon.ico')


# Configure login page
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Create api and register views
api = Api(app=app)
api_bp = Blueprint('api', __name__)

from . import view
from app.views import gallery, search, upload, contact, login

app.register_blueprint(gallery.bp)
app.register_blueprint(search.bp)
app.register_blueprint(upload.bp)
app.register_blueprint(contact.bp)
app.register_blueprint(login.bp)


# from .resources import GalleryView
# Add api resources
# api.add_resource(GalleryView, '/gallery')

# Register the API to the app
app.register_blueprint(api_bp)
