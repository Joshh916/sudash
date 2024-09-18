"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
import email_validator
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        'User Name',
        validators=[
            Length(min=4),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    username = StringField(
        'Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SearchForm(FlaskForm):
    """Torrent search form."""
    search_str = StringField(
        'Name',
        validators=[
            DataRequired()
        ]
    )
    media_type = RadioField(
        'Movie or TV Show?',
        choices=[('movie', 'Movies'), ('tv_show', 'TV Shows')],
        default='movie'
    )
    submit = SubmitField('Search')