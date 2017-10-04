from flask import Flask, Blueprint, url_for, redirect
from flask_restful import Api
from flask_login import LoginManager


# store private information in instance
app = Flask(
    __name__,
    instance_relative_config=True,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static'
)
# Load default user
app.config.from_object(
    'app.default_config.DevelopmentConfig'
)

# Start the index service
if app.config['ENABLE_SEARCH']:
    from whooshalchemy import IndexService
    si = IndexService(config=app.config)
    # if os.path.isdir(app.config['WHOOSH_BASE']):
    #     shutil.rmtree(app.config['WHOOSH_BASE'])  # fresh index from whoosh prevents errors/slowdowns


@app.route('/')
def catch_all():
    return redirect(
        url_for('gallery.index')
    )


# Avoid favicon 404
@app.route("/favicon.ico", methods=['GET'])
def favicon():
    return url_for('static', filename='favicon.ico')


# Configure login page
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login.login'

# Create api and register views
# api = Api(app=app)
# api_bp = Blueprint('api', __name__)

# from . import view
# from app.views import gallery, search, upload, contact, login, user
#
# app.register_blueprint(gallery.bp, url_prefix='/gallery')
# app.register_blueprint(search.bp, url_prefix='/search')
# app.register_blueprint(upload.bp, url_prefix='/upload')
# app.register_blueprint(contact.bp, url_prefix='/contact')
# app.register_blueprint(user.bp, url_prefix='/settings')
# app.register_blueprint(login.bp)        # This is available at the app level


# from .resources import GalleryView
# Add api resources
# api.add_resource(GalleryView, '/gallery')

# Register the API to the app
# app.register_blueprint(api_bp)
