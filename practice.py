"""Feedback Flask app."""

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, Feedback
from form import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user()

    if "username" in session:
        return redirect (f"/users/{user.username}")

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        
        user = User.Register(username , password , first_name, last_name , email)

        db.session.commit()

        session["username"] = user.username
        
        return redirect(f'/users/{user.username}')

    else:

        return render_template('register.html', form=form)    

@app.route('/login',  methods=['GET' , 'POST'])
def login_user():

    if "username" in session:
        return redirect(f"/users/{user.username}")

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username , password)
        
        if user:
            session["username"] = user.username
            return redirect('/users/{user.username}')

        else:
            form.username.errors = ["Invalid username/password"]
            return render_template('login.html', form=form)

    return render_template('login.html' , form=form)        

@app.route('/logout')
def logout():

    session.pop("username")
    return redirect('/login')


@app.route('/users/<username>')
def show_user(username):

    if "username" not in session or username != session["username"]:
        return redirect('/login')

    user = User.query.get_or_404(username)
    form = DeleteForm()

    return render_template('show.html', user=user , form=form)    


@app.route('/users/<username>/delete', methods=['POST'])
def remove_user(username):

    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()

    session.pop("username")

    return redirect('/login')    

            