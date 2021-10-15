from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.quote import Quote
from flask_app.models.messaging import Messaging
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bycrypt = Bcrypt(app)

# @app.route('/')
# def login_page():
#     return render_template('HTML HERE')

# @app.route('/login',methods=['POST'])
# def login():
#     phone_number = request.form['phone_number']
#     if not User.login_validation(phone_number):
#         flash('Invalid phone number/password')
#         return redirect ('/')
#     else:
#         data = {'phone_number':phone_number}
#     user = User.get_user(data)
#     if not user:
#         flash('Invalid username/password')
#         return redirect ('/')
#     if not bycrypt.check_password_hash(user.password,request.form['password']):
#         flash('Invalid username/password')
#         return redirect ('/')
#     session['user_id'] = user.id
#     session['phone_number'] = phone_number
#     return redirect(REDIRECT LINK HERE)

# @app.route('/register_user',methods=['POST'] )
# def registerUser():
#     pw1 = request.form['password']
#     pw2 = request.form['password_confirmed']
#     results = User.password_compare(pw1,pw2)
#     if not results:
#         return redirect('/')
#     else:
#         data = {
#             'full_name': request.form['full_name'],
#             'phone_number': request.form['phone_number'],
#             'password': bcrypt.generate_password_hash(pw1),
#         }
#     if not User.registration_validation(data):
#         return redirect('/')
#     else:
#         results = User.register_user(data)
#         user_id =  results['id']
#         session['user_id'] = user_id
#         session['phone_number'] = data['phone_number']
#         return redirect(HOMPAGE ROUTE) 

# @app.route(ROUTE HOME PAGE)
# def home_page(user_id):
#     try:
#         if (session['user_id'] == user_id):
#             user = User.get_user({'phone_number':session['phone_number']})
#             bank_accounts = Family.get_bank_accounts({'family_id':session['family_id']})
#             return render_template('TEMPLATE_HERE', user=user)
#         else:
#             return redirect('/logout')
#     except:
#         return redirect('/logout')

# @app.route('/set_requested_time')
# def registering_requested_time():
#     data = {
#         'user_id': session['user_id'],
#         'requested_time': request.form['request_time']
#     }
#     User.schedule_request_time(data)
#     flash('We have scheduled your quote time!')
#     return redirect(HOME PAGE HERE)

# @app.route('/cancel_requested_time')
# def cancel_quote_time():
#     data = {'user_id': session['user_id']}
#     User.cancel_request_time(data)
#     flash('We have cancelled your quote time. Let us know when you are ready for more motivation!')
#     return redirect(HOME PAGE HERE)

# @app.route('/one_time_quote')
# def get_one_time_quote():
#     quote = Quote.one_time_quote()
#     data = {
#         'phone': session['phone_number'],
#         'message': quote
#     }
#     Messaging.send_sms(data)
#     return redirect(HOME PAGE HERE)
