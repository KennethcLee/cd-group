from flask_app import app
from flask import flash, redirect, render_template, request
from flask_app.models.messaging import Messaging

#For testing only
@app.route("/")
def index():
    return render_template("test.html")

@app.route("/message_send", methods=['POST'])
def message_send():
    data = {
        'phone':    request.form['phone'],
        'message':  request.form['message']
    }
    print('***  100A  ***', request.form, data)
    result=Messaging.send_sms(data)
    if (result):

        flash('Message Sent')
    else:
        flash('Message NOT Sent')
    print('***  100B  ***', result) 
    return redirect("/")