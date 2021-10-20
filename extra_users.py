import re
from flask.typing import URLValuePreprocessorCallable
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_reg():
    return render_template("login_reg.html")

@app.route('/login', methods= ["POST"])
def login():
    data = {
        "phone_num": request.form["phone_num"],
        "password": request.form["password"]
    }
    user = User.get_user_by_phone_num(data)
    if not user:
        flash("Invalid email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid password")
        return redirect('/')
    session["user"] = user.id

    return redirect('/dashboard')
@app.route('/create', methods= ["POST"])
def register():
    
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "name": request.form["name"],
        "phone_num": request.form["phone_num"],
        "password": pw_hash, 
        "date_time": 0,
    }
    User.save(data)
    print(User.get_user_by_phone_num(data))
    session["user_id"] = User.get_user_by_phone_num(data).id
    return redirect('/dashboard')
@app.route('/dashboard1')
def dashboard():
    data = {
        "id": session["user_id"]
    }
    user = User.get_user_by_id(data)

    
    return render_template("dashboard.html", user = user)
@app.route('/set_time', methods= ["POST"])
def set_time():
    User.update(request.form)
    return redirect('/')