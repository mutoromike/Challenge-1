# views.py

from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def about():
    return render_template("register.html")

@app.route('/dashboard')
def about():
    return render_template("dashboard.html")

