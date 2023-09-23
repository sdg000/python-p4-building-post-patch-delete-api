#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# fetching all game instances
@app.route('/games')
def games():

    games = []
    for game in Game.query.all():
        game_dict = {
            "title": game.title,
            "genre": game.genre,
            "platform": game.platform,
            "price": game.price,
        }
        games.append(game_dict)

    response = make_response(
        games,
        200
    )

    return response

# fetching game instance by id
@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    
    game_dict = game.to_dict()

    response = make_response(
        game_dict,
        200
    )

    return response


# fetching all reviews / posting review
@app.route('/reviews', methods=['GET','POST'])
def reviews():

    # step 1: Check for various HTTP Request Method Types and handle accordingly:

    # handling GET Request
    if request.method == 'GET':

        reviews = []
        for review in Review.query.all():
            review_dict = review.to_dict()
            reviews.append(review_dict)

        response = make_response(
            reviews,
            200
        )

        return response
    
    # handling GET Request
    elif request.method == 'POST':
        
        # step 1: extract values from form to create new Review Instance
        new_review = Review(
            score=request.form.get("score"),
            comment=request.form.get("comment"),
            game_id=request.form.get("game_id"),
            user_id=request.form.get("user_id"),
        )
        # step 2: add new instance to to session and commit to session
        db.session.add(new_review)
        db.session.commit()

        # step 3: convert new instance to dictionary and return it alongside status code
        new_review_dict = new_review.to_dict()
        response = make_response(
            new_review_dict,
            201
        )

        return response
        


# view function to GET / DELETE / PATCH Review by id
@app.route('/reviews/<int:id>', methods=['GET', 'DELETE', 'PATCH'])
def find_review_by_id(id):

    # step 1: find review
    review = Review.query.filter(Review.id == id).first()

    # step 2: Define General if not found REsponse
    if not review:
        response = make_response(
            'Review not found',
            400
        )

        return response


    # step 3: Check for various HTTP Request Method Types and handle accordingly:

    # Handling GET Request
    if request.method == 'GET':
        review_dict = review.to_dict()
        response = make_response(
            jsonify(review_dict),
            200
        )
        return response


    # Handling PATCH Request
    elif request.method == 'PATCH':

        # step 1: iterate through form,  for every key in form, 
            # find corresponding key in review and set it to value of key in form
        for attr in request.form:
            setattr(review, attr, request.form.get(attr))

        # step 2: add UPDATED instance to to session and commit to session
        db.session.add(review)
        db.session.commit()

         # step 3: convert UPDATED instance to dictionary and return it alongside status code
        review_dict = review.to_dict()

        response = make_response(
            review_dict,
            200
        )

        return response

    # Handling DELETE Request
    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()

        response_body = {
            'delete_successful': True,
            'message': 'Review successful deleted.'
        }

        response = make_response(
            response_body,
            200
        )
        
        return response




# function to return all users
@app.route('/users')
def users():

    users = []
    for user in User.query.all():
        user_dict = user.to_dict()
        users.append(user_dict)

    response = make_response(
        users,
        200
    )

    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
