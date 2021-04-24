from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import random
from backend.models import setup_db, Question, Category


# ------------------------------------------------ PAGINATION -------------------------------------------------------- #
QUESTIONS_PER_PAGE = 10


# Implement pagination to only get 10 questions per page
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)  # if none default is 1
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [questions.format() for questions in selection]
    current_questions = questions[start:end]
    return current_questions


# ------------------------------------------ CREATE & CONFIGURE APP -------------------------------------------------- #
def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

# --------------------------------------- GET CATEGORIES ------------------------------------------------------------- #
    @app.route("/categories")
    def get_categories():
        try:
            categories = Category.query.all()
            categories_dict = {category.id: category.type for category in categories}

            if len(categories) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "categories": categories_dict,
                    "total_categories": len(categories),
                }, 200
            )
        except:
            abort(500)

# ------------------------------------------ GET QUESTIONS ----------------------------------------------------------- #
    @app.route("/questions")
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                abort(404)

            categories = Category.query.all()
            categories_dict = {category.id: category.type for category in categories}

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection),
                    "current_category": None,
                    "categories": categories_dict,
                }, 200
            )
        except:
            abort(500)

# --------------------------------------- DELETE QUESTION ------------------------------------------------------------ #
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(422)

            question.delete()

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "total_questions": len(Question.query.all()),
                }, 200
            )
        except:
            abort(500)

# ------------------------------------------ ADD QUESTIONS ----------------------------------------------------------- #
    @app.route("/questions", methods=["POST"])
    def add_questions():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)

        if (new_question is None) or (new_answer is None) or (new_category is None) or (new_difficulty is None):
            abort(422)

        try:
            add_question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty
            )

            add_question.insert()

            return jsonify(
                {"success": True,
                 "created": add_question.id,
                 "total_questions": len(Question.query.all()),
                 }, 200
            )
        except:
            abort(500)

# --------------------------------------- SEARCH QUESTIONS ----------------------------------------------------------- #
    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search = body.get("search_term", None)

        if not search:
            abort(400)

        try:
            search_results = Question.query.filter(Question.question.ilike("%{}%".format(search))).all()

            return jsonify(
                {
                    "success": True,
                    "questions": [questions.format() for questions in search_results],
                    "total_questions": len(search_results),
                }, 200
            )
        except:
            abort(422)

# ------------------------------------ CATEGORIES FOR EACH QUESTION -------------------------------------------------- #
    @app.route("/categories/<int:category_id>/questions")
    def get_category_questions(category_id):
        try:
            selection = Question.query.filter(Question.category == category_id).all()
            questions = paginate_questions(request, selection)

            categories = Category.query.order_by(Category.type).all()

            if len(questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "total_questions": len(Question.query.all()),
                    "current_category": category_id,
                    "categories": [category.format() for category in categories],
                }, 200
            )
        except:
            abort(500)

# --------------------------------------------- Play Quiz ------------------------------------------------------------ #
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        body = request.get_json()
        try:
            category = body.get("quiz_category", None)
            previous_questions = body.get("previous_questions", None)

            if (category is None) or (previous_questions is None):
                abort(400)

            if category["id"] == 0:
                available_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(category=category["id"]).filter(
                    Question.id.notin_(previous_questions)).all()

            if len(available_questions) > 0:
                new_question = available_questions[random.randrange(0, len(available_questions))].format()
            else:
                new_question = None

            return jsonify(
                {
                    "success": True,
                    "question": new_question,
                 }, 200
            )
        except:
            abort(500)
# --------------------------------------------- Error Handlers ------------------------------------------------------- #
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "Bad request"
            }
        ), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "Not Found"
            }
        ), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "Unprocessable Entity"
            }
        ), 422

    @app.errorhandler(405)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 405,
                "message": "Method Not Allowed"
            }
        ), 405

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify(
            {
                "success": False,
                "error": 500,
                "message": "Internal Server Error"}
        ), 500

    return app
