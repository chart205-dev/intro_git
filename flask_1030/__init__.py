from flask import Flask
app = Flask(__name__)
import flask_1030.main

from flask_1030 import db
db.create_books_table()