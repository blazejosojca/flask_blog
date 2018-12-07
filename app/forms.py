from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password',
                                            validators=[DataRequired(),
                                                        EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                    'This username already exists. Please use a different username!'
                                )

    def validat_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email already exists. Please use a different email!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UserUpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Confirm')

    
    def validate_username(self, username):
        if username.data is not current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError(
                    'This username already exists. Please use a different username!'
                                )

    def validate_email(self, email):
        if email.data is not current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('This email already exists. Please use a different email!')