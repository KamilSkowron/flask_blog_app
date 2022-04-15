from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)

# Old database
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"    

# New database
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://username:password@localhost/db_name"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password123@localhost/our_users"

# Secret Key
app.config['SECRET_KEY'] = "32k3o23ko2"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	favorite_color = db.Column(db.String(100))
	date_added = db.Column(db.DateTime, default=datetime.utcnow)

	def __rep__(self):
		return '<Name %r>' % self.name



# Create Form Class
class UserForm(FlaskForm):
	name = StringField("Name", validators=[DataRequired()])
	email = StringField("Email", validators=[DataRequired()])
	favorite_color = StringField("Favorite Color")
	submit = SubmitField("Submit")


# Create Form Class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")


# Update Database Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name =request.form['name'] # different way to handle request.form but the other one still works
		name_to_update.email =request.form['email']
		name_to_update.favorite_color =request.form['favorite_color']
		try:
			db.session.commit()
			flash("User Updated Succesfully!")
			return render_template("update.html",
									form=form,
									name_to_update=name_to_update)
		except:
			flash("Error! Looks like there was a problem, try again")
			return render_template("update.html",
									form=form,
									name_to_update=name_to_update)
	else:
		return render_template("update.html",
		form=form,
		name_to_update=name_to_update)


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form= UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data= ''
		form.email.data= ''
		form.favorite_color.data = ''
		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
							form=form,
							name=name,
							our_users=our_users)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/user/<name>')
def user(name):
	return render_template("user.html", name=name)


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form =NamerForm()
	
	#Validate From
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successfully")

	return render_template("name.html",
							name=name,
							form=form)


@app.route('/about_me')
def about_me():
	return render_template("about_me.html")

if __name__ == '__main__':
    app.run(debug=True)