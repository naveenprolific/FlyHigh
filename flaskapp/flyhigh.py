from flask import Flask,render_template,redirect,url_for,flash,request,session
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,IntegerField
from wtforms.fields.html5 import TelField
from wtforms.validators import InputRequired,Email,Length,EqualTo
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin,login_user,login_required,logout_user,current_user
import gc


app = Flask(__name__)
app.config['SECRET_KEY']='nnnsr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19918914nnn@localhost/fh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

db = SQLAlchemy(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin,db.Model):
	id = db.Column(db.Integer,primary_key = True)
	fullname = db.Column(db.String(20),unique = True) 
	username = db.Column(db.String(20),unique = True)
	email = db.Column(db.String(50),unique = True)
	password= db.Column(db.String(100),unique = True)
	phno = db.Column(db.String(11),unique = True)
	settings = db.Column(db.String(5000))
	tracking = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class signupform(FlaskForm):
	fullname = StringField('Full Name',validators=[InputRequired(),Length(min=4,max=20)])
	phno = StringField('Mobile Number',validators = [InputRequired(),Length(min=10,max=11)])
	username = StringField('Username',validators=[InputRequired(),Length(min=4,max=20)])
	email = StringField('Email',validators=[InputRequired(),Email(message='Invalid Email ID'),Length(max=50)])
	password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match'),Length(min=8,max=80)])
	confirm  = PasswordField('Confirm Password')

class loginform(FlaskForm):
	username = StringField('Username',validators=[InputRequired(),Length(min=4,max=20)])
	password = PasswordField('Password', validators=[InputRequired()])



@app.route('/')
def home():
	return render_template("main.html")

@app.route('/about/')
def about():
	return render_template("about.html")

@app.errorhandler(404)
def pagenotfound():
	return render_template("404.html")

@app.route('/signup/',methods=['GET','POST'])
def signup():
	error = ''
	try:
		form = signupform(request.form)
		if request.method == 'POST':
			newuser = User(fullname= form.fullname.data ,phno=form.phno.data ,username=form.username.data ,email=form.email.data ,password= sha256_crypt.encrypt((str(form.password.data))) ,tracking ="/bookt/")
			db.session.add(newuser)
			db.session.commit()
			gc.collect()
			login_user(newuser)
			session['loggedin']= True
			session['username'] = form.username.data
			session['fullname'] = form.fullname.data 
			session['phno'] =  form.phno.data
			session['email']= form.email.data
			return redirect(url_for("planner"))

		return render_template("signup.html",form=form,error=error)
	except Exception as e:
		error = "Duplicate values"
		return render_template("500.html",error=error)

@app.route('/login/',methods=['GET','POST'])
def login():
	error =" "
	try:
		form = loginform(request.form)
		if request.method == 'POST':
			user = User.query.filter_by(username=form.username.data).first()
			if user:
				if sha256_crypt.verify(form.password.data,user.password) :
					login_user(user)
					session['loggedin']= True
					session['username']=form.username.data
					return redirect(url_for("planner"))
			else:
				error = 'Invalid credentials'
		gc.collect()
		return render_template("login.html",error=error)

	except Exception as e:
		error = 'Invalid credentials'
		return render_template("500.html",error=e)
		
@app.route('/forget/')
def forget():
	return render_template("forget.html")

@app.route('/planner/',methods=['GET','POST'])
@login_required
def planner():
	try:
		if request.method == 'POST':
			return redirect(url_for("book"))
		return render_template("bookt.html")
	except Exception as e:
		return render_template("bookt.html")
	

@app.route('/explore/')
@login_required
def explore():
	return render_template("explore.html")

@app.route('/profile/')
@login_required
def profile():
	return render_template("profile.html")

@app.route('/bookingh/')
@login_required
def history():
	return render_template("bookingh.html")

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	session.clear()
	gc.collect()
	return render_template("logout.html")

@app.route('/book/')
@login_required
def book():
	return render_template("info.html")


if __name__ == '__main__':
	app.debug=True
	app.run()
	app.run(debug=True)