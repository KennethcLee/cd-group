from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
class User:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.phone_num = data["phone_num"]
        self.password = data["password"]
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (name, phone_num, password, date_time) VALUES (%(name)s, %(phone_num)s, %(password)s, %(date_time)s)"
        return connectToMySQL("group_project").query_db(query, data)
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL("group_project").query_db(query, data)
        return cls(result[0])
    @classmethod
    def get_user_by_phone_num(cls, data):
        query = "SELECT * FROM users WHERE phone_num = %(phone_num)s"
        result = connectToMySQL("group_project").query_db(query, data)
        return cls(result[0])
    @classmethod
    def get_user_by_password(cls, data):
        query = "SELECT * FROM users WHERE password %(password)s"
        result = connectToMySQL("group_project").query_db(query, data)
        return cls(result[0])
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET date = %(date)s WHERE id = %(id)s"
        return connectToMySQL("group_project").query_db(query, data)
    @staticmethod
    def validate_register(user):
        valid = True
        if not len(user["name"]) > 3:
            flash("Full name must be 4 characters long")
            valid = False
        if not len(user["phone_num"]) == 10:
            flash("Phone number must be 10 digits long")
            valid = False
        if User.get_user_by_phone_num(user):
            flash("Phone number already exists")
            valid = False
        if not user["password"] == user["password_confirm"]:
            flash("Passwords do not match")
            valid = False
        return valid

