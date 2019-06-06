from flask_wtf import FlaskForm
from flask_babel import _
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app.models import Post


class PostForm(FlaskForm):
    title = StringField(_('Title'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired(), Length(min=2)])
    status = SelectField('Post status',
                         choices=(
                             (Post.STATUS_PUBLIC, 'Public'),
                             (Post.STATUS_DRAFT, 'Draft')),
                         coerce=int
                         )
