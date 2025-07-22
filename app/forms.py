from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired

class IssueForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location (Address or Coordinates)', validators=[DataRequired()])
    category = SelectField('Category', choices=[('pothole', 'Pothole'), ('lights', 'Broken Streetlight'), ('rubbish', 'Rubbish Collection')], validators=[DataRequired()])
    image_file = FileField('Upload Photo')
    submit = SubmitField('Report Issue')