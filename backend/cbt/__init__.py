import json
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from psycopg2 import DatabaseError
from models import setup_db, Question, Category
import cloudinary, cloudinary.uploader
from dotenv import load_dotenv
import os
app = Flask(__name__)

setup_db(app)

CORS(app, resources={'/': {'origins': '*'}})

load_dotenv()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response


@app.route('/')
def index():
    return jsonify({
        'success': True
    })


@app.route('/categories')
def get_category():
    categories = Category.query.all()

    return jsonify({
        'success': True,
        'category': [category.format() for category in categories]
    })


@app.route('/categories', methods=['POST'])
def create_category():
    body = request.get_json()
    new_category = body.get('category', None)

    if (new_category == ''):
        abort(422)
    try:
        category = Category(type=new_category)
        print(category.type)
        
        category.insert()
        return jsonify({
            'success': True,
            'message': 'Category has been added!'
        }), 201
    except:
        abort(422)


@app.route('/questions')
def get_questions():
    questions = Question.query.all()
    return jsonify({
        "success": True,
        "questions": [question.format() for question in questions]
    })


@app.route('/questions', methods=['POST'])
@cross_origin()
def create_question():
    # body = request.get_json()
    # question = body.get('question', None)
    # a = body.get('a', None)
    # b = body.get('b', None)
    # c = body.get('c', None)
    # d = body.get('d', None)
    # category = body.get('category', None)
    # answer = body.get('answer', None)
    # image_link = body.get('image_link', None)
    
    # MOCK Data
    question = 'Who is seyi?'
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    category = 'Person'
    answer = 'answer'

    app.logger.info('in upload route')


    cloudinary.config(
        cloud_name = os.getenv('cloud_name'), 
        api_key=os.getenv('api_key'), 
        api_secret=os.getenv('api_secret')
    )

    upload_result = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        app.logger.info('%s file_to_upload', file_to_upload)
        if file_to_upload:
            upload_result = cloudinary.uploader.upload(file_to_upload)
            app.logger.info(upload_result)
        # return jsonify(upload_result)
    print("url is:", upload_result.get("url"))
    
    # VERIFY BEFORE ADDING QUESTION TO DB
    if (question == '') or (answer == '') or (category == '') or (a == '') or (b == '') or (c == '') or (d == ''):
        abort(422)

    try:
        question = Question(question=question, answer=answer,
                            category=category, a=a, b=b, c=c, d=d,
                            image_link=upload_result.get("url"))
        question.insert()

        return jsonify({
            'success': True,
            'message': 'Question has been added!'
        }), 201
    except:
        abort(422)

# DELETE QUESTION


@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    try:
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:
            abort(404)
        else:
            question.delete()

        return jsonify({
            'success': True,
            'deleted': question_id,
            'total_questions': len(Question.query.all())
        })
    except:
        abort(422)


if __name__ == '__main__':
    app.run(debug=True)
