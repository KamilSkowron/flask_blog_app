from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create Form Posts
class PostForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	content = StringField("Content", validators=[DataRequired()], widget=TextArea())
	author = StringField("Author")
	slug = StringField("Slugfield", validators=[DataRequired()])
	submit = SubmitField("Submit", validators=[DataRequired()])

# Create Form Class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	username = StringField("Username", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favorite_color = StringField("Favorite Color")
	about_author = TextAreaField("About Author")
	password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match!')])
	password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
	profile_pic = FileField ("Profile Pic")
	submit = SubmitField("Submit")

# Create Password Form Class
class PasswordForm(FlaskForm):
	email = StringField("What's Your email?", validators=[DataRequired()])
	password_hash = PasswordField("What's Your password?", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create A Search Form
class SearchFrom(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")