# views.py
from flask import Flask, render_template, flash, redirect, url_for, request, session
from app.Models.user import User
from app import app
import validators
#app = Flask(__name__)
app.secret_key = "super secret key"

userdetails = {}

def create_new_user(username, email, password, confirm_password):
    if username in userdetails:
        error = 'Username already exists'
    if email in userdetails:
        error = 'email already exists'    
    if validators.email(email) != True:
        error = 'Enter a valid email'
    if len(password) < 5:
        error = 'Password should be more than four characters'
    if password != confirm_password:
        error = 'The two passwords should match'   
    global userdetails
    account = User(username, email, password, confirm_password)
    userdetails = account

@app.route('/')#route to the index file
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])#route to handle requests to the login
def login():
    error = None 
    global userdetails

    if request.method == 'POST':
       
        name = request.form['username']
        pswd = request.form['password']
        if name in userdetails:
            if pswd in userdetails:
                session['logged_in'] = True
                return redirect(url_for('dashboard')) 
            else:
                error = 'Invalid credentials'       
        else:
            error = 'Invalid Credentials'      
    return render_template("login.html")
    
    

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username     = request.form['username']
        email       = request.form['email']
        password    = request.form['password']
        confirm_password = request.form['confirm_password']
        
        new = create_new_user(username, email, password, confirm_password)
        return redirect('/dashboard')
    return render_template('register.html')


