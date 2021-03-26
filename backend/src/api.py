import os
from flask import Flask, request, jsonify, abort, redirect, url_for
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,PATCH')
    return response

@app.route('/')
def welcome():
    return 'app started'

@app.route('/login')
def login():
    return redirect('https://coffeeshopprojectudacity.us.auth0.com/authorize?audience=coffeeshop&response_type=token&client_id=MkxM5Va8rVqLJdNp2tWDr4378AdzdNDm&redirect_uri=http://localhost:8100/tabs/user-page')

@app.route('/login-results')
def loginResults():
    return 'You are logged in successfully'

@app.route('/logout')
def logout():
    return redirect('https://coffeeshopprojectudacity.us.auth0.com/v2/logout?client_id=MkxM5Va8rVqLJdNp2tWDr4378AdzdNDm&returnTo=http://localhost:5000/logout-results')

@app.route('/logout-results')
def logoutResults():
    return redirect(url_for('login'))

'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    drinkList = Drink.query.all()
    drinks = [ drinks.short() for drinks in drinkList]
    return jsonify({
        "success" : True,
        "drinks" : drinks
    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
def get_drinks_detail():
    drinkList = Drink.query.all()
    drinks = [ drinks.long() for drinks in drinkList]
    return jsonify({
        "success" : True,
        "drinks" : drinks
    })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink():

    id = request.get_json()['id']
    recipe = request.get_json()['recipe']
    recipeJson =  json.dumps(recipe) 
    print("type of recipe: ", type(recipeJson))
    title = request.get_json()['title']
    print("id: ", id)
    print("recipe: ", recipeJson)
    print("title: ", title)
    print("request: ", request.json)
    drink = Drink( recipe=recipeJson, title=title)
    drink.insert()
    drinkList = Drink.query.all()
    drinks = [ drinks.long() for drinks in drinkList]
    return jsonify({
        "success" : True,
        "drinks" : drinks
    })
    
    
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:ID>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(ID):
    id = request.get_json('id')
    recipe = request.get_json()['recipe']
    recipeJson =  json.dumps(recipe) 
    title = request.get_json()['title']
    drink = Drink.query.filter_by(id=ID).first()    
    drink.id= ID
    drink.recipe=recipeJson
    drink.title = title
    drink.update()
    return jsonify({
        "success" : True,
        "drinks": drink.long()
    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:ID>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(ID):
   
    drink = Drink.query.filter_by(id=ID).first()
    drink.delete()
    return jsonify({
        "success" : True,
        "delete": ID
    })

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
