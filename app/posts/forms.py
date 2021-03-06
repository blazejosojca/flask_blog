from flask_wtf import FlaskForm, Form
from flask_babel import _
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from app.models import Post


class PostForm(FlaskForm):
    title = StringField(_('Title'), validators=[DataRequired()])
    content = TextAreaField(_('Content'), validators=[DataRequired(), Length(min=2)])
    status = SelectField('Post status',
                         choices=(
                             (Post.PUBLIC_STATUS, 'Public'),
                             (Post.DRAFT_STATUS, 'Draft'),
                             ), coerce=int)


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
