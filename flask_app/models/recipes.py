from re import S
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.under30 = data['under30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.user_id = data['user_id']

    #CREATE ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, under30, description, instructions, date_made, user_id) VALUES (%(name)s, %(under30)s, %(description)s, %(instructions)s, %(date_made)s, %(user_id)s)"
        new_recipe_id = connectToMySQL('recipes_schema').query_db(query, data)
        return new_recipe_id

    #UPDATE-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #READ (One) (by ID)
    @classmethod
    def get_recipe_by_id(cls, data):
        #data = {"id": "1"}
        print(data)
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        print(result)
        rcp = result[0]
        #Changing date format
        rcp['date_made'] = rcp['date_made'].strftime("%B, %d, %Y")
        recipe = cls(rcp)
        return recipe

    #UPDATE 
    @classmethod
    def update_recipe(cls, form):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s ,date_made=%(date_made)s, user_id=%(user_id)s WHERE recipes.id=%(id)s"
        result = connectToMySQL('recipes_schema').query_db(query, form)
        return result

    #DELETE ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def delete_recipe(cls, data):
        #data = {"id": "1"}
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        return result


    #READ (ALL) -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes"
        result = connectToMySQL('recipes_schema').query_db(query)
        recipes = []
        for r in result:
            recipe = cls(r)
            recipes.append(recipe)
        return recipes

    #VALIDATE -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        #Validar que mi nombre de la receta sea mayor a 3 caracteres
        if len(recipe['name']) < 3:
            flash('Name must have at least 3 characters', 'recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description must have at least 3 characters', 'recipe')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions must have at least 3 characters', 'recipe')
            is_valid = False
        if recipe['date_made']=="":
            flash('Pick up a date', 'recipe')
            is_valid = False
        return is_valid
