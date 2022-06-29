from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
import re

db = "car_dealz_db"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class user: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def new_user(cls, data):
        query = "INSERT INTO car_dealz_db.users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        return cls(results[0])

    @staticmethod
    def check_stats(user):
        is_valid = True 
        if len(user['first_name']) < 3:
            flash(u"First Name is not long enough!!", 'first_name_len')
            is_valid = False
        if len(user['last_name']) < 3:
            flash(u"Last Name is not long enough!!", 'last_name_len')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash(u"Invalid email address!", 'email')
            is_valid = False
        if len(user['password']) < 8:
            flash(u"Password is not long enough!!", 'password_len')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash(u"Passwords do not match", 'password_match')
            is_valid = False
        return is_valid

    @classmethod
    def get_all_users(cls, id):
        query = "SELECT * FROM car_dealz_db.users WHERE NOT id = %(id)s ORDER BY first_name ASC;"
        results = connectToMySQL(db).query_db(query, {'id': id})
        users = []
        for user in results:
            users.append(cls(user))
        return users