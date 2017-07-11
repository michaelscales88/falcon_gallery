from flask import Flask, Blueprint
from flask_restful import Api
from flask_login import LoginManager


# store private information in instance
app = Flask(__name__, instance_relative_config=True, template_folder='templates')

# Load default settings
app.config.from_object('app.default_config.DevelopmentConfig')

# Start the index service
if app.config['ENABLE_SEARCH']:
    from whooshalchemy import IndexService
    si = IndexService(config=app.config)


# Configure login page
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# Create api and register views
api = Api(app=app)
api_bp = Blueprint('api', __name__)

from . import view
from app.views import gallery, search, upload

app.register_blueprint(gallery.bp)
app.register_blueprint(search.bp)
app.register_blueprint(upload.bp)


# from .resources import GalleryView
# Add api resources
# api.add_resource(GalleryView, '/gallery')

# Register the API to the app
app.register_blueprint(api_bp)
