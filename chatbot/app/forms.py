# coding: utf-8
from flask_wtf import Form
from wtforms import SubmitField, TextField
from wtforms.validators import Required


class QuestionForm(Form):
	question = TextField('Question', validators=[Required()])
	send = SubmitField('Send')