# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## Endpoints
```
GET '/categories'
GET '/questions?page=<page_number>'
POST '/questions'
POST '/questions/search'
DELETE '/questions/<question_id>'
GET '/categories/<category_id>/questions'
POST '/quizzes'
```

### GET '/categories'
* Returns all categories:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": "True",
  "total_categories": 6,
  "code": 200
}
```

### GET '/questions?page=<page_number>'
* Returns 10 questions in the current page:
```json
{
  "categories": {
    "1": "Science",
    "2": "Art"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Application Programming Interface",
      "category": 1,
      "difficulty": 3,
      "id": 10,
      "question": "What is an API?"
    },
    {
      "answer": "Application Programming Interface",
      "category": 1,
      "difficulty": 3,
      "id": 10,
      "question": "What is an API?"
    }
  ],
  "success": "True",
  "total_questions": 12,
  "code": 200
}
```

### POST '/questions'
* Create a new Question
```json
{
  "created": 13,
  "total_questions": 13,
  "success": "True",
  "code": 200
}
```

### POST '/questions/search'
* Returns all questions (10 per page) that are similar to search term
```json
{
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": "True",
  "total_questions": 1,
  "code": 200
}
```

### DELETE '/questions/<question_id>'
* Deletes the question of the question id
```json
{
  "deleted": 10,
  "success": "True",
  "total_questions": 12,
  "code": 200
}
```

### GET '/categories/<category_id>/questions'
* Retrieves all the question of the given category
```json
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "current_category": 1,
  "questions": [
    {
      "answer": "Application Programming Interface",
      "category": 1,
      "difficulty": 3,
      "id": 10,
      "question": "What is an API?"
    },
    {
      "answer": "Application Programming Interface",
      "category": 1,
      "difficulty": 3,
      "id": 10,
      "question": "What is an API?"
    }
  ],
  "success": "True",
  "total_questions": 12,
  "code": 200
}
```

### POST '/quizzes'
* Retrieves a question that has not already been asked to play the quiz 
```json
{
  "questions": [
    {
      "answer": "Application Programming Interface",
      "category": 1,
      "difficulty": 3,
      "id": 10,
      "question": "What is an API?"
    }
    ],
  "success": "True",
  "code": 200
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```