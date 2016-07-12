# coding: utf-8
from . import app, db
from flask import render_template

@app.route('/')
def index():
    return 'index'
