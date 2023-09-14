from flask import render_template, session, request, redirect
from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['POST'])
def create_user():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
    user_id =User.save(data)
    session ['id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def logged_in():
    if not User.validate_login(request.form):
        return redirect('/')
    print(request.form)
    data = {
        'email' : request.form['email']
    }
    db_user = User.get_by_email(data)
    session ['id'] = db_user.id
    session ['first_name'] = db_user.first_name
    session ['email'] = db_user.email
    return redirect('/dashboard')

@app.route('/dashboard')
def welcome():
    if "id" not in session:
        return redirect ('/logout')
    data ={
        'id' : session['id']
    }
    user= User.get_by_id(data)
    return render_template("login.html", user = user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")