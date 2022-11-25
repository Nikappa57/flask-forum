from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

from wtforms import (validators, BooleanField, StringField, 
    SubmitField, TextAreaField, SelectField, IntegerField)

from Site.models.rank import Rank
from Site.views.Forum.src.messages import Error


class CategoryForm(FlaskForm):
    name = StringField('Title', validators=[
        validators.InputRequired(Error.required),
        validators.Length(min=3, max=60, message=
            Error.length.format(name='title', min=3, max=60))])

    position = IntegerField('Position', validators=[
        validators.InputRequired(Error.required)])

    submit = SubmitField('Confirm')

class SectionForm(FlaskForm):
    name = StringField('Title', validators=[
        validators.InputRequired(Error.required),
        validators.Length(min=3, max=60, message=
            Error.length.format(name='title', min=3, max=60))])

    desc = TextAreaField('Description', validators=[
        validators.InputRequired(Error.required),
        validators.Length(min=3, max=1024, message=
            Error.length.format(name='description', min=3, max=1024))])


    position = IntegerField('Position', validators=[
        validators.InputRequired(Error.required)])
    
    priority_required = SelectField('Rank required', 
        choices=[(rank.priority, rank.name) for rank in Rank.query.all()],
        coerce=int, 
        validators=[validators.InputRequired(Error.required)])
    
    priority_require_to_create = SelectField('Rank required to create a Thread', 
        choices=[(rank.priority, rank.name) for rank in Rank.query.all()],
        coerce=int, 
        validators=[validators.InputRequired(Error.required)])

    submit = SubmitField('Confirm')

class ThreadForm(FlaskForm):
    title = StringField('Title', validators=[
        validators.InputRequired(Error.required),
        validators.Length(min=3, max=60, message=
            Error.length.format(name='title', min=3, max=60))])

    text = TextAreaField('Text', validators=[
        validators.InputRequired(Error.required),
        validators.Length(min=5, max=1024, message=
            Error.length.format(name='text', min=3, max=1024))])

    img = FileField('img', validators=[FileAllowed(['jpg', 'jpg', 'png'])])

    pinned = BooleanField('Pinned')

    submit = SubmitField('Confirm')

class CommentsForm(FlaskForm):
    text = TextAreaField('Text', validators=[
        validators.InputRequired(Error.required),
        validators.Length(min=2, max=1024, message=
            Error.length.format(name='text', min=2, max=1024))])

    submit = SubmitField('Confirm')

