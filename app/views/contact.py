from flask import Blueprint, render_template, request, redirect, url_for, g
from app.user import User


bp = Blueprint('contact', __name__)


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/<string:author>', methods=['GET'])
@bp.route('?=<string:author>', methods=['GET', 'POST'])
def index(author=''):

    # author-choice form
    authors = g.session.query(User).all()

    if not author and request.method == 'POST':
        print('POST')
        # Form select author
        selected_author = request.form.get('author')
        if selected_author:
            # Render stuff for author
            return redirect(url_for('contact.index', author=selected_author))

    print(author)
    if author:
        # Url select author
        print('found GET', author)
        selected_author = g.session.query(User).filter(User.alias == author).first()
    else:
        print('Default')
        selected_author = g.session.query(User).first()

    image_results = [img for img in selected_author.images]
    return render_template(
        'contact/contact.html',
        title='Contact',
        authors=authors,
        selected_author=selected_author,
        image_results=image_results
    )
