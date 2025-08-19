from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length

# Admin Login Form (username-based)
class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Issue Form (create/edit issues)
class IssueForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=120)])
    description = TextAreaField("Description", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("pothole", "Pothole"),
            ("lights", "Lights"),
            ("rubbish", "Rubbish"),
            ("water", "Water"),
            ("other", "Other")
        ],
        validators=[DataRequired()]
    )
    status = SelectField(
        "Status",
        choices=[
            ("open", "Open"),
            ("in_progress", "In Progress"),
            ("resolved", "Resolved")
        ],
        default="open",
        validators=[DataRequired()]
    )
    image_filename = FileField("Upload Image (optional)")
    submit = SubmitField("Save")

