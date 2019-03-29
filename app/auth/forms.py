from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_babel import _, lazy_gettext as _l
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(_l('Username', validators=[DataRequired(),                                                     Length(min=2, max=24)]))
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField(_l('Password', validators=[DataRequired()]))
    password_confirmation = PasswordField(_l('Confirm Password',
                                          validators=[DataRequired(), EqualTo('password')]))
    submit = SubmitField(_l('Sign Up'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                    _l('This username already exists. Please use a different username!')
                                )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l('This email already exists. Please use a different email!'))


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class UpdateUserForm(FlaskForm):
    username = StringField(_l('Username'),
                           validators=[DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    image_file = FileField(_l('Update profile picture'),
                           validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data is not self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different username!'))

    def validate_email(self, email):
        if email.data is not self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError(_l('Please use a different email!'))


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class DeleteUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=24)]
                           )
    submit = SubmitField('Delete User')

