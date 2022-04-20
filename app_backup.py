from flask import Flask, redirect, render_template, flash, request, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from datetime import datetime, date

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, PostForm, UserForm, PasswordForm, NamerForm

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


# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))



#------------------------# Routes #------------------------#

@app.route('/')
def index():
	return render_template('index.html')

#-------------------# Posts #-------------------#

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		post = Posts(title=form.title.data,
					 content=form.content.data,
					 author=form.author.data,
					 slug=form.slug.data)
		# Clear the Form
		form.title.data = ""
		form.content.data = ""
		form.author.data = ""
		form.slug.data = ""

		# Add post data to database
		db.session.add(post)
		db.session.commit()

		flash("Blog Post Submitted Successfully!")

	return render_template("add_post.html",form=form)

# Edit post
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.author = form.author.data
		post.slug = form.slug.data
		post.content = form.content.data
		
		# Update Database
		db.session.add(post)
		db.session.commit()
		flash("Post has been updated.")
		return redirect(url_for('post', id=post.id))
	
	form.title.data = post.title
	form.author.data = post.author
	form.slug.data = post.slug
	form.content.data = post.content
	return render_template('edit_post.html', form=form)

# Delete post
@app.route('/posts/delete/<int:id>')
def delete_post(id):
	post = Posts.query.get_or_404(id)

	try:
		db.session.delete(post)
		db.session.commit()
		flash("Post was deleted.")
		return redirect(url_for('posts'))
	except:
		flash("Something gone wrong")
		return redirect(url_for('posts'))
	
# Single post
@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)

@app.route('/posts')
def posts():
	# Grab all the post from the database
	posts = Posts.query.order_by(Posts.date_posted)
	return render_template("posts.html", posts=posts)


#-------------------# User #-------------------#

# Add User
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form= UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:

			# Hash the password
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256")

			user = Users(name=form.name.data,
						 username=form.username.data, 
						 email=form.email.data, 
						 favorite_color=form.favorite_color.data, 
						 password_hash=hashed_pw)

			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data= ''
		form.username.data= ''
		form.email.data= ''
		form.favorite_color.data = ''
		form.password_hash.data = ''
		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
							form=form,
							name=name,
							our_users=our_users)

# Edit User
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name =request.form['name'] # different way to handle request.form but the other one still works
		name_to_update.email =request.form['email']
		name_to_update.favorite_color =request.form['favorite_color']
		name_to_update.username = request.form['username']
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
		name_to_update=name_to_update,
		id=id)

# Delete User
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
	form = UserForm()
	name = None

	user_to_delete = Users.query.get_or_404(id)
	
	try:
		db.session.delete(user_to_delete)
		db.session.commit()
		flash("User deleted successfully!")

		our_users = Users.query.order_by(Users.date_added)
		return render_template("add_user.html",
							form=form,
							name=name,
							our_users=our_users)

	except:
		flash("Something gone wrong...")
		return render_template("add_user.html",
					form=form,
					name=name,
					our_users=our_users)


#-------------------# Login #-------------------#

# Create Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Succesfull")
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again")
		else:
			flash("That user doesn't exist.")
			
	return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You have been logout!")
	return redirect(url_for('login'))

# Create Dashboard Page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	id = current_user.id
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name =request.form['name'] # different way to handle request.form but the other one still works
		name_to_update.email =request.form['email']
		name_to_update.favorite_color =request.form['favorite_color']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Succesfully!")
			return render_template("dashboard.html",
									form=form,
									name_to_update=name_to_update)
		except:
			flash("Error! Looks like there was a problem, try again")
			return render_template("dashboard.html",
									form=form,
									name_to_update=name_to_update)
	else:
		return render_template("dashboard.html",
		form=form,
		name_to_update=name_to_update,
		id=id)
	
#-------------------# Error handlers #-------------------#

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500


#-------------------# Random staff #-------------------#

# Json Thing
@app.route('/date')
def get_current_date():
	favourite_pizza = {
		"John":"Pepperoni",
		"Mary":"Cheese",
		"Tim":"Mushrooms"
	}
	return favourite_pizza
	#return {"Date": date.today()}


@app.route('/user/<name>')
def user(name):
	return render_template("user.html", name=name)

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


@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None

	form =PasswordForm()
	
	#Validate From
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the form
		form.email.data = ''
		form.password_hash.data = ''
		
		# Lookup User by email
		pw_to_check = Users.query.filter_by(email=email).first()

		# Check Hashed Password
		passed = check_password_hash(pw_to_check.password_hash, password)	#(hashed password, password from the form) #True/False


	return render_template("test_pw.html",
							email=email,
							password=password,
							pw_to_check=pw_to_check,
							passed=passed,
							form=form)


@app.route('/about_me')
def about_me():
	return render_template("about_me.html")




#------------------------# Models #------------------------#



class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), nullable=False, unique=True)
	name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False, unique=True)
	favorite_color = db.Column(db.String(100))
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	
	#Do some password stuff
	password_hash = db.Column(db.String(128))


	#It doesn't allow see written password (It's forbitten)
	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute!')
	
	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self,password):
		return check_password_hash(self.password_hash, password)



	def __rep__(self):
		return '<Name %r>' % self.name

# Create a Blog Post model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	author = db.Column(db.String(255))
	date_posted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))



if __name__ == '__main__':
    app.run(debug=True)