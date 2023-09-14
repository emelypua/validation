from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re	
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = 'login_and_registration'
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('login_and_registration').query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users( first_name , last_name , email , password , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW() );"
        return connectToMySQL(cls.DB).query_db( query, data )
    
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])

    @staticmethod
    def validate_register(user):
        is_valid = True 
        
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { 'email' : user['email'] }
        results = connectToMySQL(User.DB).query_db(query, data)
        if len(results) >= 1:
            flash("Email already exists.", "reg")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email, please use another email.", "reg")
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "reg")
            is_valid = False
        if len(user['last_name']) <2:
            flash("Last name must be at least 2 characters.", "reg")
            is_valid = False
        if len(user['password']) <8:
            is_valid = False
            flash("Password must be at least 8 characters.", "reg")
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Passwords must match.", "reg")
        return is_valid
    
    @staticmethod
    def validate_login( user ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = { 'email' : user['email'] }
        results = connectToMySQL(User.DB).query_db(query, data)
        print(len(results))
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address! Try again.", "login")
            is_valid = False
            return is_valid
        if len(results) < 1:
            flash("Email or password is incorrect, try again", "login")
            is_valid = False
        if not bcrypt.check_password_hash(results[0]['password'],user['password']):
            flash("Invalid Email/Password", "login")
            is_valid = False   
        return is_valid