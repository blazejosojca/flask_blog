from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CreatePostForm(FlaskForm):
    title = StringField(_('Title'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired(), Length(min=2)])
    submit = SubmitField(_('Create Post'))


class UpdatePostForm(CreatePostForm):
    submit = SubmitField(_('Update Post'))
