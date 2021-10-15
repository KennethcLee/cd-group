import datetime
from flask_app.config.mysqlconnection import connectToMySQL




db = 'motivational_app'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.full_name = data['full_name']
        self.phone_number = data['phone_number']
        self.password = data['password']
        self.requested_time = data['requested_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.quotes_id = data['quotes_id']

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
