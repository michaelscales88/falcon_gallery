from flask import Blueprint, render_template, request, redirect, url_for, g
from app.models.user import User


bp = Blueprint('contact', __name__)    # , static_folder='static' , template_folder='templates'


@bp.route('/contact', methods=['GET', 'POST',])
@bp.route('/contact/<author>', methods=['GET'])
def index(author=''):
    # author-choice form
    authors = g.session.query(User).all()

    if author or request.method == 'POST':
        # Show specific author
        select = request.form.get('author')
        if select:
            # Render stuff for author
            print('select author for contacts', select)
            return redirect(url_for('contact.index'))

    return render_template(
        'contact.html',
        title='Contact',
        authors=authors
    )
