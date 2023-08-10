from flask import render_template, request, redirect, url_for
from application import app, db
from application import bcrypt

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html', title='Home')