# forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MovieForm(FlaskForm):
    title = StringField('Movie Title', 
    validators=[DataRequired(), 
    Length(min=1, max=100, 
    message="Title must be between 1 and 100 characters")])
    
    description = TextAreaField('Movie Description', 
    validators=[DataRequired(), 
    Length(min=10, 
    message="Description must be at least 10 characters")])
    
    poster = FileField('Movie Poster', 
    validators=[DataRequired(), 
    FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Submit')