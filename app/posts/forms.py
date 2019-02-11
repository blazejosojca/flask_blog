from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Create Post')


class UpdatePostForm(CreatePostForm):
    submit = SubmitField('Update Post')
