from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#CREATE -----------------------------------------------------
@app.route('/recipes/new')
def new_recipe():
    return render_template('add_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name": request.form['name'],
        "under30" :request.form['under30'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "user_id": session['user_id']
    }
    
    Recipe.create_recipe(data)
    return redirect('/dashboard')


#UPDATE -----------------------------------------------------
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    data = {
        "id": id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('edit_recipe.html', recipe=recipe)


@app.route('/recipes/update', methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/')

    if not Recipe.validate_recipe(request.form):
            return redirect('/dashboard')
    data = {
        "id":request.form['id'],
        "name": request.form['name'],
        "under30" :request.form['under30'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "user_id": session['user_id']
    }
    Recipe.update_recipe(data)
    return redirect('/dashboard')


#DELETE -----------------------------------------------------------
@app.route('/recipes/delete/<int:id>')
def delete_recipe(id):
    data = {
        "id": id
    }
    Recipe.delete_recipe(data)
    return redirect('/dashboard')

 
#SHOW -----------------------------------------------------------------
@app.route('/recipes/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": id
    }
    recipe = Recipe.get_recipe_by_id(data)

    data2 = {
        "id": session['user_id']
    }
    user= User.get_user_by_id(data2)
    return render_template('show_recipe.html', recipe=recipe, user=user)
