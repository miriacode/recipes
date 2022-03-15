from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')

#REGISTER ---------------------------------------------------------------
@app.route("/register", methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')

    pwd = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }
    id = User.create_user(data)
    #Session starts
    session['user_id'] = id
    return redirect('/dashboard')

#LOGIN -----------------------------------------------------------------
@app.route("/login", methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("Email not found", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect Password", "login")
        return redirect('/')
    #Session starts
    session['user_id'] = user.id
    return redirect('/dashboard')


#DASHBOARD ------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "id": session['user_id']
    }
    user = User.get_user_by_id(data)
    recipes = Recipe.get_all_recipes()
    print(recipes)
    return render_template('dashboard.html', user=user,recipes=recipes)

#LOGOUT -------------------------------------------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')