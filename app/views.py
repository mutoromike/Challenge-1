# views.py
from flask import Flask, render_template, flash, redirect, url_for, request, session
from app.models.user import user
from app import app
app = Flask(__name__)
app.secret_key = "super secret key"

def signup():
    userdetails = {'username': 'username', 'email': 'email', \
                    'password': 'password'}
    user = userdetails               
    return user

create_user = {}

@app.route('/')#route to the index file
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])#route to handle requests to the login
def login():
    error = None 
      
    if request.method == 'POST':
       
        name = request.form['username']
        pswd = request.form['password']
        if name in mine and pswd in mine:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))        
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
        
        if email not in mine:
            if password == confirm_password:
                mine['username'] = username
                mine['email'] = email
                mine['password'] = password
                flash('Signup successful, you can now create a shopping list')
                session['logged_in'] = False
                return redirect(url_for('login'))
            else:
                error = 'Passwords do not match'
        else:
            error = 'Email already in use'
    return render_template('register.html')


