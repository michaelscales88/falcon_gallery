from flask import render_template, g, Blueprint, url_for, redirect
from flask_login import login_required


bp = Blueprint('search', __name__)


@bp.route('/search', methods=['POST'])
@login_required
def index():
    if not g.search_form.validate_on_submit():
        print('search.index submitted')
        return redirect(url_for('index.index'))
    return redirect(url_for('search.search_results', query=g.search_form.search.data))


@bp.route('/search_results/<query>')
@bp.route('/search_results/<query>/<int:page>', methods=['GET', 'POST'])
def search_results(query, page=1):
    return render_template(
        'search_results.html',
        query=query
    )