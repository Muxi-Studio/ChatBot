# coding: utf-8

import os
import pymongo
from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'

host = os.environ.get('MONGODB_URL')
conn = pymongo.Connection(host=host,port=27017)
db = conn.chatbot

from . import views, forms
