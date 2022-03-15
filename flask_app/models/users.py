from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash

class User:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []
    
    #FOR REGISTER------------------------------------------------------------------------------------------------------------
    #CREATE
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        new_user_id = connectToMySQL('recipes_schema').query_db(query, data)
        return new_user_id


    #VALIDATE
    @staticmethod
    def validate_user(user):
        # user = {
        #     "first_name": "Emilio",
        #     "last_name": "Navejas",
        #     "email": "emilio@codingdojo.com"
        #     "password": .............
        #     "confirm": .............
        # }
        is_valid = True
        #Check if the first name has more than 2 characters
        if len(user['first_name']) < 2:
            flash('First name should have at least 2 characters', 'registrer')
            is_valid = False
        #Check if the last name has more than 2 characters
        if len(user['last_name']) < 2:
            flash('Last name should have at least 2 characters', 'register')
            is_valid = False
        #Validate email with regex
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email', 'register')
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match", 'register')
            is_valid = False
        #Check if the email already exists
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recipes_schema').query_db(query, user)
        if len(results) >= 1:
            flash('Email has been already registered', 'register')
            is_valid = False
        return is_valid

    #FOR LOGIN ------------------------------------------------------------------------------------------------------------
    #READ (ONE) (By email) 
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        if len(result) < 1:
            return False
        else :
            usr = result[0]
            user = cls(usr)
            return user

    #DFOR DASHBOARD ------------------------------------------------------------------------------------------------------------
    #READ (ONE) (By ID)
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        usr = result[0]
        user = cls(usr)
        return user

    @classmethod
    def get_all(cls):
        query =" SELECT * FROM users"
        results = connectToMySQL('recipes_schema').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users