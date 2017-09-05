# views.py
from flask import Flask, render_template, flash, redirect, url_for, request, session
from app.Models.user import User
from app import app
import validators
#app = Flask(__name__)
app.secret_key = "super secret key"

userdetails = {}
app.username_list = []
app.email_list = []
app.passwords_list = []

def create_new_user(username, password, email):      
    global userdetails
    account = User(username, email, password)
    userdetails[username] = account
    return userdetails

@app.route('/')#route to the index file
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])#route to handle requests to the login
def login():
    global userdetails
    error = None
    if request.method == 'POST':
       
        name = request.form['username']
        pswd = request.form['password']
        if name in app.username_list:
            if pswd in app.passwords_list:
                session['logged_in'] = True
                session['id'] = name
                return redirect(url_for('dashboard')) 
            else:
                error = 'Wrong Password'       
        else:
            error = 'Username Does not exist'      
    return render_template("login.html", error=error)    

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
        if username not in app.username_list:
            if email not in app.email_list:
                if validators.email(email):
                    if len(password) > 5:
                        if password == confirm_password:         
                            new = create_new_user(username, email, password)
                            app.username_list.append(username)
                            app.email_list.append(email)
                            app.passwords_list.append(password)
                            userdetails = new
                            return redirect('/login')
                        else:
                            error = 'The two passwords should match'
                    else:    
                        error = 'Password should be more than five characters'
                else:    
                    error = 'Enter a valid email'   
            else:
                error = 'Email has already been used'
        else:
            error = 'Username has already been used'
    return render_template('register.html', error=error)


