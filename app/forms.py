from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])


class SaveForm(FlaskForm):
    file_name = StringField('file_name')



