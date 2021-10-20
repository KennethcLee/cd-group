from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.quote import Quote
from flask_app.models.messaging import Messaging
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login_reg.html')

@app.route('/login',methods=['POST'])
def login():
    phone_number = f"+1{request.form['phone_num']}"
    if not User.login_validation(phone_number):
        flash('Invalid phone number format. Use 10 digit number with no dashes or spaces. EX: 5463541234')
        return redirect ('/')
    else:
        data = {'phone_number':phone_number}
    user = User.get_user(data)
    if not user:
        flash('Invalid phone number/password')
        return redirect ('/')
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash('Invalid phone number/password')
        return redirect ('/')
    session['user_id'] = user.id
    session['phone_number'] = phone_number
    return redirect(f'/{user.id}/dashboard')

@app.route('/register_user',methods=['POST'] )
def registerUser():
    pw1 = request.form['password']
    pw2 = request.form['password_confirm']
    results = User.password_compare(pw1,pw2)
    if not results:
        return redirect('/')
    else:
        phone_number = f"+1{request.form['phone_num']}"
        data = {
            'full_name': request.form['name'],
            'phone_number': phone_number,
            'password': bcrypt.generate_password_hash(pw1),
        }
    if not User.registration_validation(data):
        return redirect('/')
    else:
        results = User.register_user(data)
        user_id =  results['id']
        session['user_id'] = user_id
        session['phone_number'] = data['phone_number']
        return redirect(f'/{user_id}/dashboard')

@app.route('/<int:user_id>/dashboard')
def home_page(user_id):
    try:
        if (session['user_id'] == user_id):
            user = User.get_user({'phone_number':session['phone_number']})
            return render_template('dashboard.html', user=user)
        else:
            return redirect('/')
    except:
        return redirect('/')

    user = User.get_user({'phone_number':session['phone_number']})
    return render_template('dashboard.html', user=user)

@app.route('/set_requested_time', methods=['POST'])
def registering_requested_time():
    user_id = session['user_id']
    request_time = request.form['time']
    time_zone = request.form['time-zone']
    time = User.convert_time(request_time,time_zone)
    data = {
        'user_id': user_id,
        'requested_time': time,
        'time_zone': time_zone
    }
    User.schedule_request_time(data)
    flash('We have scheduled your quote time!')
    return redirect(f'/{user_id}/dashboard')

@app.route('/cancel_requested_time')
def cancel_quote_time():
    user_id = session['user_id']
    data = {'user_id': user_id}
    User.cancel_request_time(data)
    flash('We have cancelled your quote time. Let us know when you are ready for more motivation!')
    return redirect(f'/{user_id}/dashboard')

@app.route('/one_time_quote')
def get_one_time_quote():
    user_id = session['user_id']
    quote = Quote.one_time_quote()
    data = {
        'phone': session['phone_number'],
        'message': quote
    }
    Messaging.send_sms(data)
    flash('We have sent your one time quote!')
    return redirect(f'/{user_id}/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 
