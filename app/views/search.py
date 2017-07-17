from flask import render_template, Blueprint, url_for, redirect, request
from app.models import User, Image
bp = Blueprint('search', __name__)


@bp.route('/search', methods=['POST'])
def index():
    query = request.form.get('search')
    if query:
        return redirect(url_for('search.search_results', query=query))
    return redirect(url_for('gallery.index'))


@bp.route('/search_results/<query>')
@bp.route('/search_results/<query>', methods=['GET', 'POST'])
def search_results(query):
    user_query = User.search_query(query)
    image_query = Image.search_query(query)
    user_results = []
    image_results = []
    for user in user_query:
        user_results += [img for img in user.images]
    for image in image_query:
        image_results.append(image)
    return render_template(
        'search_results.html',
        query=query,
        user_results=user_results,
        image_results=image_results
    )