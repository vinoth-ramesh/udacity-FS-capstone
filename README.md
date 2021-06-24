# Full Stack Developer Capstone Project

## Casting Agency

The Casting Agency Project models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 
 
### Database Setup to run locally

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
dropdb casting_test
created casting_test
```

Then run the DB upgrade step to create the objects in the DB:
```bash
python manage.py db upgrade
```

Once the objects are created logon to DB and create some dummy records for testing (This step is optional)
```bash
psql -d casting_test <username>

insert into movies (title, release_date) values ('Avengers','2021-06-21' );
insert into actors (name, age, gender, movie_id) values ('Tom Cruse', 39, 'Male', 1);
```

### Running the server

From the base directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### To run the test case locally

Execute the python unit test script using the below command:
```bash
python test_app.py
```

### Hosted Application and Roles:

There are three roles within the API. Casting Assistant, Casting Director and Executive Producer. The logins for the three roles has been provided in the file [role_token.json][https://github.com/vinoth-ramesh/udacity-FS-capstone/blob/main/role_token.json]

The url for the API: https://casting-udacity.herokuapp.com/


### ENDPOINTS
GET '/movies'
GET '/actors'
DELETE '/movies/<int:movie_id>'
DELETE '/actors/<int:actor_id>'
POST '/movies'
POST '/actors'
PATCH '/movies/<int:movie_id>'
PATCH '/actors/<int:actor_id>'

GET '/movies'
- Fetches all the movies present in the DB
- Request Arguments: None
- Returns: The movie details with the actors associated with it. 
```
[
    {
        "actors": [
            {
                "age": 40,
                "gender": "Male",
                "id": 1,
                "movie_id": 1,
                "name": "Robert Brown"
            }
        ],
        "id": 1,
        "release_date": "Sun, 12 Jan 2020 00:00:00 GMT",
        "title": "Avengers Marvel"
    }
]
```

GET '/actors'
- Fetches all the actors present in the DB
- Request Arguments: None
- Returns: 
```
[
    {
        "age": 40,
        "gender": "Male",
        "id": 1,
        "movie_id": 1,
        "name": "Robert Brown"
    }
]
```

DELETE '/movies/<int:movie_id>
- Delete an existing movie in the DB
- Request Arguments: int:movie_id
- Returns:
```
{
    "message": "Movie Deleted",
    "success": true
}
```

DELETE '/actors/<int:actor_id>
- Delete an existing actor in the DB
- Request Arguments: int:actor_id
- Returns:
```
{
    "message": "Actor Deleted",
    "success": true
}
```

POST '/movies'
- Add a new movie to the DB
- Request Arguments: title:string, release_date:date
- Returns:
```
{
    "created": 2,
    "new_movie": {
        "actors": [],
        "id": 2,
        "release_date": "Mon, 21 Jun 2021 00:00:00 GMT",
        "title": "Avengers"
    },
    "success": true
}
```

POST '/actors'
- Add a new actor to the DB
- Request Arguments: name:string, age:int, gender:string, movie_id:int
- Returns:
```
{
    "created": 3,
    "new_actor": {
        "age": 36,
        "gender": "Male",
        "id": 3,
        "movie_id": 2,
        "name": "Matt Damon"
    },
    "success": true
}
```

PATCH '/movies/<int:movie_id>'
- Update details for the given movie (movie_id)
- Request Arguments: int:movie_id and any combination of parameters from post method for movies
- Returns:
```
{
    "message": "Movie Updated",
    "success": true
}
```

PATCH '/movies/<int:actor_id>'
- Update details for the given actor (actor_id)
- Request Arguments: int:actor_id and any combination of parameters from post method for actors
- Returns:
```
{
    "message": "Actor Updated",
    "success": true
}
```