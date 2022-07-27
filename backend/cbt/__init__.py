from flask import Flask
from flask_cors import CORS
from models import setup_db, Question, Category

app = Flask(__name__)

setup_db(app)

CORS(app, resources={'/': {'origins': '*'}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS,PATCH')
    return response

@app.route('/')
def index():
    return "DONE!"
    
if __name__ == '__main__':
    app.run(debug=True)
