# coding: utf-8
from . import app, api
from flask import Flask, render_template

@app.route('/', methods=['GET','POST'])
def index():
	return render_template("home.html")
