
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Actor, Movie, setup_db
from flaskr import create_app
from models import db
import datetime


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()

        self.new_movie = {
            'title': 'My Movie',
            'release_date': datetime.date(2021, 6, 21)
        }

        self.update_movie = {
            'title': 'Old Movie',
            'release_date': datetime.date(2020, 6, 21)
        }

        self.new_actor = {
            'name': 'Rocky Rambo',
            'age': 41,
            'gender': 'Male',
            'movie_id': 1
        }

        self.update_actor = {
            'name': 'Vin Diesel',
            'age': 35
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Set up authentication tokens info
        with open('role_token.json', 'r') as f:
            self.auth = json.loads(f.read())

        assistant_jwt = self.auth["roles"]["Casting Assistant"]["jwt_token"]
        director_jwt = self.auth["roles"]["Casting Director"]["jwt_token"]
        producer_jwt = self.auth["roles"]["Executive Producer"]["jwt_token"]

        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }

    def tearDown(self):
        pass

    def test_create_movie(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], 'My Movie')

    def test_create_actor(self):
        header_obj = {"Authorization": self.auth_headers["Casting Director"]}
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor']['name'], 'Rocky Rambo')

    def test_get_movies(self):
        header_obj = {"Authorization": self.auth_headers["Casting Assistant"]}
        res = self.client().get('/movies', headers=header_obj)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_fail(self):
        header_obj = {"Authorization": self.auth_headers["Casting Assistant"]}
        res = self.client().get('/moviess', headers=header_obj)
        self.assertEqual(res.status_code, 404)

    def test_get_actors(self):
        header_obj = {"Authorization": self.auth_headers["Casting Assistant"]}
        res = self.client().get('/actors', headers=header_obj)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_fail(self):
        header_obj = {"Authorization": self.auth_headers["Casting Assistant"]}
        res = self.client().get('/actorss', headers=header_obj)
        self.assertEqual(res.status_code, 404)

    def test_patch_movie(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().patch('/movies/1', json=self.update_movie,
                                  headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_fail(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().patch('/movies/2000', json=self.update_movie,
                                  headers=header_obj)
        self.assertEqual(res.status_code, 404)

    def test_patch_actor(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().patch('/actors/1', json=self.update_actor,
                                  headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_fail(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().patch('/actors/2000', json=self.update_actor,
                                  headers=header_obj)
        self.assertEqual(res.status_code, 404)

    def test_delete_actor_fail(self):
        header_obj = {"Authorization": self.auth_headers["Casting Director"]}
        res = self.client().delete('/actors/1000', headers=header_obj)
        self.assertEqual(res.status_code, 404)

    def test_delete_actor(self):
        header_obj = {"Authorization": self.auth_headers["Casting Director"]}
        res = self.client().delete('/actors/2', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_fail(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().delete('/movies/1000', headers=header_obj)
        self.assertEqual(res.status_code, 404)

    def test_delete_movie(self):
        header_obj = {"Authorization": self.auth_headers["Executive Producer"]}
        res = self.client().delete('/movies/2', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


if __name__ == "__main__":
    unittest.main()
