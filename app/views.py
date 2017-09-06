# views.py
from flask import Flask, render_template, flash, redirect, url_for, request, session
from app.Models.user import User
from app.Models.shopping_list import Shoppinglist
from app import app
import validators
#app = Flask(__name__)
app.secret_key = "super secret key"

app.userdetails = {}
app.username_list = []
app.email_list = []
app.passwords_list = []
app.shoppinglist = {}

def create_new_user(username, password, email):      
    account = User(username, email, password)
    app.userdetails[id] = account
    return app.userdetails

def add_shoppinglist(name, user_id):#name and desc
    shoppinglist_obj = Shoppinglist(name)

    if user_id not in app.shoppinglist:
        # app.shoppinglist[user_id] = {new_shoppinglist.id: new_shoppinglist}
        app.shoppinglist[user_id] = []
        app.shoppinglist[user_id].append(shoppinglist_obj.name)
    else:
        app.shoppinglist[user_id].append(shoppinglist_obj.name)
    return True

def get_username_id(username):
    for user in app.userdetails:
        if app.userdetails[user].username == username:
            return app.userdetails[user].id

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
                flash('Login successful')
                return redirect(url_for('dashboard')) 
            else:
                error = 'Wrong Password'       
        else:
            error = 'Username Does not exist'      
    return render_template("login.html", error=error)    

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard(): 
    if request.method == 'POST':
        shoppinglist = request.form['shoppinglist']
        user_id = session['id']
        add_shoppinglist(shoppinglist, user_id)
        flash('List added successful.') 
        return redirect(url_for('shoppinglist'))  
    return render_template("dashboard.html")

@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    session.pop('username', None)
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
                            new = create_new_user(username, email, password,)
                            app.userdetails[username] = new
                            app.username_list.append(username)
                            app.email_list.append(email)
                            app.passwords_list.append(password)
                            flash('User successfully created')
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

@app.route('/shoppinglist')
def shoppinglist():
    # shoppinglists = None if session['id'] not in app.shoppinglist else app.shoppinglist.values()
    if app.shoppinglist == {}:
        list_name = ''
    elif app.shoppinglist[session['id']]:
        list_name = app.shoppinglist[session['id']]
        print(list_name)
            # return render_template('lists.html', shoppinglists=list_name)
    # else:
    #     list_name = None
    
    return render_template('lists.html', shoppinglists=list_name)


