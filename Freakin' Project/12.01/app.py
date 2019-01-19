from flask import Flask, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
from hashlib import sha256

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)




def render_str(template,**params):
   t = jinja_env.get_template(template)
   return t.render(params)

def render(template, **kw):
   return render_str(template, **kw)

def check_user(name, password):
	user = User.query.filter_by(username = name).first()
	if user:
		return sha256(password.encode('utf-8')).hexdigest() == user.password
	else:
		return False

@app.route("/register" , methods=['GET', 'POST'])
def register ():
	if request.method == 'GET':
		return render("register.html")
	if request.method == "POST":
		name = request.form['login']
		password = request.form['password']
		user = User(username=name, password = sha256(password.encode('utf-8')).hexdigest())
		db.session.add(user)
		db.session.commit()
		return "<h1> Success!! </h1>"

@app.route("/login" , methods=['GET', 'POST'])
def login ():
	if request.method == 'GET':
		return render("login.html")
	if request.method == "POST":
		name = request.form['login']
		password = request.form['password']
		if check_user(name, password):
			session['name'] = name
			session['password'] = password
			return "<h1> Welcome, %s</h1>" % name
		else:
			return render('login.html', error = "You're not exist")



app.secret_key = 'f9d103a28f0b5aaf9f116e7a06f280025a644ce76c01042268f9c49611aa9d1f'
if __name__ == '__main__':
	app.run(debug = True)