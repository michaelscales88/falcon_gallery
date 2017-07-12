from flask import render_template, g, Blueprint, url_for, redirect, request


bp = Blueprint('search', __name__)


@bp.route('/search', methods=['POST'])
def index():
    select = request.form.get('search')
    if select:
        return redirect(url_for('search.search_results', query=select))
    return redirect(url_for('gallery.index'))


@bp.route('/search_results/<query>')
@bp.route('/search_results/<query>/<int:page>', methods=['GET', 'POST'])
def search_results(query, page=1):
    return render_template(
        'search_results.html',
        query=query
    )