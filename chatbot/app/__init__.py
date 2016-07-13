# coding: utf-8

import os
import pymongo
from flask import Flask

try:
    from pymongo.connection import Connection
except ImportError as e:
    from pymongo import MongoClient as Connection


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

host = os.environ.get('MONGODB_URL')
conn = Connection(host=host,port=27017)
db = conn.chatbot

from . import views, forms
