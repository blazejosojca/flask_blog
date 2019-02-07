from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=24)]
                           )
    email = StringField('Email', validators=[DataRequired(),
                                             Email()]
                        )
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password',
                                          validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                    'This username already exists. Please use a different username!'
                                )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email already exists. Please use a different email!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateUserForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    image_file = FileField('Update profile picture',
                           validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data is not self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username!')

    def validate_email(self, email):
        if email.data is not self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email!')


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Create Post')


class UpdatePostForm(CreatePostForm):
    submit = SubmitField('Update Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with this email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
