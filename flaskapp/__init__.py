from flask import Flask,render_template,redirect,url_for,flash,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']='nnnsr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:19918914nnn@localhost/flyhigh'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =True

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	fullname = db.Column(db.String(20),unique = True) 
	username = db.Column(db.String(20),unique = True)
	email = db.Column(db.String(50),unique = True)
	password= db.Column(db.String(100),unique = True)
	phno = db.Column(db.Integer,unique = True)
	settings = db.Column(db.String(5000))
	tracking = db.Column(db.String(100))

	

@app.route('/')
def home():
	return render_template("main.html")

@app.route('/about/')
def about():
	return render_template("about.html")

@app.route('/signup/',methods=['GET','POST'])
def signup():
	return render_template("signup.html")

@app.route('/login/',methods=['GET','POST'])
def login():
	error =" "
	try:
		if request.method == 'POST':
			username = request.form['username']
			password = request.form['password']	
			if username == 'naveen' and password == 'nnnsr' :
				return redirect(url_for('planner'))
			else:
				error = " Invalid Credentials Entered !.. Try Again .."
		return render_template("login.html",error=error)

	except Exception as e:
		return render_template("login.html",error=error)
		
@app.route('/forget/')
def forget():
	return render_template("forget.html")

@app.route('/planner/')
def planner():
	return render_template("bookt.html")

@app.route('/explore/')
def explore():
	return render_template("explore.html")

@app.route('/profile/')
def profile():
	return render_template("profile.html")

@app.route('/bookingh/')
def history():
	return render_template("bookingh.html")

@app.route('/logout/')
def logout():
	return render_template("logout.html")

@app.route('/book/')
def book():
	return render_template("info.html")


if __name__ == '__main__':
	app.debug=True
	app.run()
	app.run(debug=True)