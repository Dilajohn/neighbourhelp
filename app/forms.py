from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField



class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class IssueForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    location = StringField(
        "Location (Address or Coordinates)", validators=[DataRequired()]
    )
    category = SelectField(
        "Category",
        choices=[
            ("pothole", "Pothole"),
            ("lights", "Broken Streetlight"),
            ("rubbish", "Rubbish Collection"),
        ],
        validators=[DataRequired()],
    )
    image_file = FileField("Upload Photo")
    submit = SubmitField("Report Issue")
