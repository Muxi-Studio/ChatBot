from flask import Flask
from flask import jsonify
from . import app, db
from flask import render_template, redirect, url_for, request, session
from flask import request, jsonify
from forms import QuestionForm
import jieba
import jieba.analyse
import jieba.posseg as pseg
jieba.load_userdict("dic.txt")


@app.route('/gettxt/<keyword>', methods=['GET'])
def gettxt(keyword):
    adict = db.txt.find({'index': keyword})
    for i in adict:
        tag = i['tag']
        index = i['index']
        content = i['content']
        return jsonify({
            'tag':tag,
            'index':index,
            'content':content
        })

@app.route('/getweb/<keyword>', methods=['GET'])
def getweb(keyword):
    adict = db.web.find({'index': keyword})
    for i in adict:
        tag = i['tag']
        index = i['index']
        content = i['content']
        return jsonify({
            'tag':tag,
            'index':index,
            'content':content
        })

@app.route('/getpic/<keyword>', methods=['GET'])
def getpic(keyword):
    adict = db.pic.find({'index': keyword})
    for i in adict:
        tag = i['tag']
        index = i['index']
        content = i['content']
        return jsonify({
            'tag':tag,
            'index':index,
            'content':content
        })
        