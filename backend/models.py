import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

database_name = 'cbt'
database_path = 'postgresql://{}:{}@{}/{}'.format(
                os.environ.get('DB_USER'),
                os.environ.get('DB_PASS'),'localhost:5432', 
                database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    category = Column(String)
    a = Column(String)
    b = Column(String)
    c = Column(String)
    d = Column(String)
    answer = Column(String)
    image_link = Column(String)
   

    def __init__(self, question, a, b, c, d, image_link, answer, category):
        self.question = question
        self.category = category
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.answer = answer
        self.image_link = image_link

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'd': self.d,
            'image_link': self.image_link
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }