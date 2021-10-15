from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.quote import Quote
from flask_app.models.user import User



#for testing only
@app.route('/')
def load_homepage():
    return render_template('test.html')



