from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length

# Admin Login Form (replaces the duplicated LoginForm)
class AdminLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# Issue Form (for editing/creating issues in admin)
class IssueForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=3, max=120)])
    description = TextAreaField("Description", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("Roads", "Roads"),
            ("Lighting", "Lighting"),
            ("Waste", "Waste"),
            ("Water", "Water"),
            ("Other", "Other")
        ],
        validators=[DataRequired()]
    )
    status = SelectField(
        "Status",
        choices=[
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Resolved", "Resolved")
        ],
        default="Pending",
        validators=[DataRequired()]
    )
    image_filename = FileField("Upload Image (optional)")
    submit = SubmitField("Save")


