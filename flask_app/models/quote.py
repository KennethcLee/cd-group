from datetime import date

from flask.globals import request
from flask_app.config.mysqlconnection import connectToMySQL
from flask import jsonify
import requests
import random

db = 'motivational_app'

class Quote:
    def __init__(self, data):
        self.id = data['id']
        self.text = data['text']
        self.author = data['author']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    #gets unique quote by refrencing db of given user. Returns unique quote to user and adds the user-quote relationship to db
    def get_quote(cls,user_id):
        previous_quotes = []
        number = random.randint(1,1642)
        data = {'user_id':user_id}
        
        query = "SELECT quote_id FROM users_received_quotes WHERE user_id = %(user_id)s;"
        results = connectToMySQL(db).query_db(query,data)
        
        for result in results:
            previous_quotes.append(result['quote_id'])
        
        while number in previous_quotes:
            number = random.randint(1,1642)
        
        data = {
            'quote_id': number,
            'user_id': user_id
            }
        
        query = 'SELECT text, author FROM quotes WHERE id = %(quote_id)s;'
        quote = connectToMySQL(db).query_db(query,data)
        
        query = 'INSERT INTO users_received_quotes(user_id,quote_id) VALUES (%(user_id)s,%(quote_id)s)'
        connectToMySQL(db).query_db(query,data)
        return quote[0] 

    @staticmethod
    #gets one time quote
    def one_time_quote():
        number = random.randint(1,1642)
        data = {'quote_id':number}
        query = 'SELECT * FROM quotes WHERE id = %(quote_id)s;' 
        results = connectToMySQL(db).query_db(query,data)
        result = results[0]['text']
        return result

    @staticmethod
    #Checks quotes DB and fills if empty
    def fill_DB():
        query = 'SELECT * FROM quotes;'
        results = connectToMySQL(db).query_db(query)
        if not results:
            responses = requests.get('https://type.fit/api/quotes')
            responses = responses.json()
            for response in responses:
                query = 'INSERT INTO quotes (text,author,created_at,updated_at) VALUES (%(text)s,%(author)s,NOW(),NOW());'
                connectToMySQL(db).query_db(query,response)
        return None
