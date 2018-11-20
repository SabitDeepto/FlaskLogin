from flask import Flask, render_template, redirect, url_for, flash 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'itssecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
	id =  db.Column(db.Integer, primary_key = True)
	user = db.Column(db.String(30))
	email =  db.Column(db.String(30))
	passw =  db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired('this is required')])
	password = PasswordField('password', validators=[InputRequired()])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	username = StringField('username', validators=[InputRequired('this is required'), Length(min=5, max=30)])
	email = StringField('Email',validators=[InputRequired('this is required'),])
	password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=30)])


##index page
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


##registration
@app.route('/signup',methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():
		hash_pass = generate_password_hash(form.password.data)
		new_user = User(user = form.username.data, email = form.email.data, passw = hash_pass)
		db.session.add(new_user)
		db.session.commit()

		return redirect(url_for('login'))
	
	return render_template("signup.html", form=form)


##login
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(user = form.username.data).first()
		if user:
			if check_password_hash(user.passw, form.password.data):
				login_user(user, remember = form.remember.data)
				return redirect(url_for('dashboard'))
		return "Invalid username or password"

	return render_template("login.html", form=form)


##Dashboard

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template("dashboard.html", name= current_user.user)


##logout
@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(debug=True)
