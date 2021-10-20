import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

phone_regex = "\w{10}"
name_regex = re.compile(r'^[a-zA-Z_\s-]+$')

db = 'motivational_app'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.phone_number = data['phone_number']
        self.password = data['password']
        self.requested_time = data['requested_time']
        self.time_zone = data['time_zone']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.previous_quotes = []

    @classmethod
    #Creates a user in the DB. Does not include a request time
    def register_user(cls, data):
        query = 'INSERT INTO users(full_name,phone_number,password,created_at,updated_at) VALUES (%(full_name)s,%(phone_number)s,%(password)s,NOW(),NOW());'
        connectToMySQL(db).query_db(query,data)
        query = 'SELECT * FROM users WHERE phone_number = %(phone_number)s;'
        results = connectToMySQL(db).query_db(query,data)
        return results[0]
    
    @classmethod
    # Gets current hour, sets end time to one hour from now, pulls users whose requested text time is in the current hour and returns all requestors
    def text_recipients(cls):
        d1 = datetime.datetime.utcnow()
        d2 = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)


        start_time = d1.strftime("%H:%M")
        start_time = f'{start_time}:00'
        
        end_time = d2.strftime("%H:%M")
        end_time = f'{end_time}:00'
        
        data = {
            'start_time': start_time,
            'end_time': end_time
            }
        
        query = "SELECT * FROM users WHERE requested_time >= %(start_time)s AND requested_time < %(end_time)s;"
        results = connectToMySQL(db).query_db(query,data)
        return results

    @classmethod
    #Gets a user and all quotes they have previously received
    def get_user(cls,data):
        query = 'SELECT * FROM users WHERE phone_number = %(phone_number)s' 
        user_results =  connectToMySQL(db).query_db(query,data)
        for user_result in user_results:
            user_data = {
                'id': user_result['id'],
                'full_name': user_result['full_name'],
                'phone_number' : user_result['phone_number'],
                'password': user_result['password'],
                'time_zone': user_result['time_zone'],
                'requested_time': user_result['requested_time'],
                'created_at': user_result['created_at'],
                'updated_at': user_result['updated_at']
            }
        user = User(user_data)
        if user.requested_time:
            user.requested_time = User.revert_time(user.requested_time,user.time_zone)
        query = 'SELECT * FROM users_received_quotes WHERE user_id = %(user_id)s ORDER BY id DESC LIMIT 5;'
        data = {'user_id': user.id }
        quotes_results = connectToMySQL(db).query_db(query,data)
        for quote_result in quotes_results:
            query = "SELECT * FROM quotes WHERE id = %(quote_id)s;"
            data = {'quote_id': quote_result['quote_id']}
            q_results = connectToMySQL(db).query_db(query,data)
            for q_result in q_results:
                user.previous_quotes.append(q_result)
        return user

    @classmethod
    #Schedules reoccuring text time
    def schedule_request_time(cls, data):
        query = 'UPDATE users SET requested_time = %(requested_time)s, time_zone = %(time_zone)s WHERE id = %(user_id)s;'
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    #Removes reoccuring text time
    def cancel_request_time(cls, data):
        query = 'UPDATE users SET requested_time = NULL, time_zone = NULL WHERE id = %(user_id)s;'
        return connectToMySQL(db).query_db(query,data)

    @staticmethod
    #Validates that a phone number is 12 digits
    def login_validation(phone_number):
        is_valid = True
        if len(phone_number) != 12:
            is_valid = False
        return is_valid

    @staticmethod
    #validates that the password meets the required minimum and the confirm matches
    def password_compare(pw1,pw2):
        if len(pw1) < 8:
            flash('Passwords must be a mininum of 8 characters.')
            return False
        elif pw1 != pw2:
            flash('Passwords must match.')
            return False
        else:
            return True

    @staticmethod
    #validates users signing up for texts
    def registration_validation(data):
        is_valid = True
        query = 'SELECT id FROM users where phone_number = %(phone_number)s'
        results = connectToMySQL(db).query_db(query,data)
        if len(results) > 0:
            flash('This phone number is already registered.')
            is_valid = False
            return is_valid
        if len(data['full_name']) < 4:
            flash('Full name must be at least 4 letters long.')
            is_valid = False
        if not name_regex.match(data['full_name']):
            flash("Full name must only be letters.")
            is_valid = False
        if len(data['phone_number']) != 12:
            flash('Invalid phone number format. Use 10 digit number with no dashes or spaces. EX: 5463541234')
            is_valid = False
        if data['password'] == False:
            is_valid = False
        return is_valid

    @staticmethod
    def convert_time(time,timeZone):
        hour = time[0]+time[1]
        min = time[3]+time[4]
        if timeZone == 'eastern':
            hour = int(hour)+ 4
        if timeZone == 'central':
            hour = int(hour)+ 5
        if timeZone == 'mountain':
            hour = int(hour)+ 6
        if timeZone == 'pacific':
            hour = int(hour)+ 7
        if timeZone == 'alaskan':
            hour = int(hour)+ 8
        if timeZone == 'hawaiian':
            hour = int(hour)+ 10
        if hour > 24:
            hour -= 24
        time = f'{hour}:{min}:00'
        
        return time

    @staticmethod
    def revert_time(time,time_zone):
        time = str(time)
        if len(time) == 8:
            hour = time[0]+time[1]
            min = str(time[3])+str(time[4])
        else:
            hour = time[0]
            min = str(time[2])+str(time[3])
        hour = int(hour)
        if time_zone == 'eastern':
            hour = hour - 4
        if time_zone == 'central':
            hour = hour - 5
        if time_zone == 'mountain':
            hour = hour - 6
        if time_zone == 'pacific':
            hour = hour - 7
        if time_zone == 'alaskan':
            hour = hour - 8
        if time_zone == 'hawaiian':
            hour = hour - 10
        if hour < 1:
            hour+=24
        if hour == 24:
            hour -= 12
            time = f'{hour}:{min} AM'
        if hour > 12:
            hour -= 12
            time = f'{hour}:{min} PM'
        else: 
            time = f'{hour}:{min} AM'
        return time



