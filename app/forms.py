from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
