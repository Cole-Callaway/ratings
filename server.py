"""Movie Ratings."""

from atexit import register
from urllib import request
from jinja2 import StrictUndefined

from flask import Flask, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template('homepage.html')

@app.route('/users')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@app.route('/register', methods=['POST'])
def register_form():
    return render_template('register_form.html')

@app.route('/register', methods = ['POST'])
def register_process():
    
    email = register_form['email']
    password = register_form['password']
    age = int(request.form['age'])
    zipcode = request.form['zipcode']
    
    new_user = User(email=email, password=password, age=age, zipcode=zipcode)
    
    db.session.add(new_user)
    db.session.commit()
    
    flash(f'user {email} added.')
    return redirect('/')

@app.route('/login', methods = ['GET'])
def login_form():
    return render_template('login_form.html')

@app.route('/login', methods = ['POST'])
def login_process():
    
    email = request.form['email']
    password = request.form['password']
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('No such user')
        
    if user.password != password:
        flash('Incorrect password')
        return redirect('/login')
    
    session['user_id'] = user.user_id
    
    flash('Logged in')
    return redirect(f'/user/{user.user_id}')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
