import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, db
from auth.authorize import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.debug = True
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
      return response


  @app.route('/movies')
  @requires_auth('view:movies')
  def get_movies(payload):
      all_movies = Movie.query.all()
      movies_format = [movie.format() for movie in all_movies]
      for movie in movies_format:
        movie['actors'] = [i.format() for i in movie['actors']]

      return jsonify(movies_format)
  

  @app.route('/actors')
  @requires_auth('view:actors')
  def get_actors(payload):
      all_actors = Actor.query.all()
      actors_format = [actor.format() for actor in all_actors]
      return jsonify(actors_format)


  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_new_movie(payload):
      body = request.get_json()

      title = body.get('title', None)
      release_date = body.get('release_date', None)

      if title is None or release_date is None:
          abort(400, "Missing field for Movie")

      movie = Movie(title=title, release_date=release_date)
      movie.insert()

      new_movie = Movie.query.get(movie.id)
      new_movie = new_movie.format()

      return jsonify(
        {
        'success': True,
        'created': movie.id,
        'new_movie': new_movie
        }
      )


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_new_actor(payload):
      body = request.get_json()

      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      movie_id = body.get('movie_id', None)

      if name is None or age is None or gender is None or movie_id is None:
          abort(400, "Missing field for Actor")

      actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
      actor.insert()

      new_actor = Actor.query.get(actor.id)
      new_actor = new_actor.format()

      return jsonify(
        {
        'success': True,
        'created': actor.id,
        'new_actor': new_actor
        }
      )


  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      
      if movie is None:
          abort(404, "No movie with given id " + str(movie_id) + " is found")

      movie.delete()

      return jsonify(
        {
        "success": True,
        "message" : "Movie Deleted"
        }
      )


  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if actor is None:
        abort(404, "No actor with given id " + str(actor_id) + " is found")

      actor.delete()

      return jsonify(
        {
        "success": True,
        "message" : "Actor Deleted"
        }
      )


  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('update:actors')
  def patch_actor(payload, actor_id):

      actor=Actor()
      actor = Actor.query.filter(Actor.id== actor_id).one_or_none()

      if actor is None:
        abort(404, "No actor with given id " + str(actor_id) + " is found")

      body = request.get_json()

      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      movie_id = body.get('movie_id', None)

      if name:
          actor.name = name
      if age:
          actor.age = age
      if gender:
          actor.gender = gender
      if movie_id:
          actor.movie_id = movie_id

      actor.update()

      return jsonify(
        {
        "success": True,
        "message": "Actor Updated"
        }
      )


  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('update:movies')
  def patch_movie(payload, movie_id):

      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if movie is None:
        abort(404, "No movie with given id " + str(movie_id) + " is found")

      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)

      movie.title = title
      movie.release_date = release_date

      movie.update()

      return jsonify(
        {
        "success": True,
        "message": "Movie Updated"
        }
      )

  @app.errorhandler(401)
  def not_found(error):
      return jsonify(
        {
        'success': False,
        'error' : 401,
        'message' : 'Authorzation header Issue'
        }
      ), 401

  @app.errorhandler(404)
  def not_found(error):
      return jsonify(
        {
        'success': False,
        'error' : 404,
        'message' : 'Resource Not Found'
        }
      ), 404


  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify(
        {
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
        }
      )     

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)