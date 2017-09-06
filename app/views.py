# views.py
from flask import Flask, render_template, flash, redirect, url_for, request, session
from app.Models.user import User
from app.Models.lists import Listitems
from app.Models.shopping_list import Shoppinglist
from app import app
import validators
import uuid
# from datetime import datetime, date
#app = Flask(__name__)
app.secret_key = "super secret key"

app.userdetails = {}
app.username_list = []
app.email_list = []
app.passwords_list = []
app.shoppinglist = {}
app.item_list = {}

def create_new_user(username, password, email):      
    account = User(username, email, password)
    app.userdetails[username] = []
    app.userdetails[username] = account
    return app.userdetails

def add_shoppinglist(name, user_id, id = None):#name and desc
    # created_time =' datetime.date.now()'
    # print(created_time)
    # Created_time = created_time.strftime("%Y-%m-%d %H:%M")
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

def create_new_item(shoppinglist, name):
    itemlist_obj = Listitems(name)
    if shoppinglist not in app.item_list:
        app.item_list[shoppinglist] = []
        app.item_list[shoppinglist].append(itemlist_obj.name)
    else:
        app.item_list[shoppinglist].append(itemlist_obj.name)
    return True


@app.route('/', methods=['GET', 'POST'])#route to handle requests to the login
def login():
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
    return render_template("index.html", error=error)    

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard(): 
    if request.method == 'POST':
        shoppinglist = request.form['shoppinglist']
        user_id = session['id']
        add_shoppinglist(shoppinglist, user_id)
        flash('List added successful.') 
        return redirect(url_for('shoppinglist'))  
    return render_template("dashboard.html")

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = request.form['additem']
        user_id = session['id']
        shoppinglist = app.shoppinglist
        
        create_new_item(shoppinglist, item)
        flash('item added successfully.') 
        return redirect(url_for('added_items'))  
    return render_template("list_items.html")

@app.route('/added_items')
def added_item():
    if app.item_list == []:
        list_name = ''
    elif app.item_list[app.shoppinglist]:
        list_name = app.item_list[app.shoppinglist]
        print(list_name)
    
    return render_template('items.html', itemlists=list_name)

@app.route('/logout')
def logout():
    """User logout/authentication/session management."""
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

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
                            return redirect('/')
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
    if app.shoppinglist == {}:
        list_name = ''
    elif app.shoppinglist[session['id']]:
        list_name = app.shoppinglist[session['id']]
        print(list_name)
    
    return render_template('lists.html', shoppinglists=list_name)


