# coding: utf-8
from . import app, db, api
from flask import render_template, redirect, url_for, request, session
from flask import request, jsonify
from forms import QuestionForm
import jieba
import jieba.analyse
import jieba.posseg as pseg
jieba.load_userdict("dic.txt")

@app.route('/', methods=['GET','POST'])
def index():
    form = QuestionForm()
    question = None
    tag = None
    keyword = None
    keydict = {}
    maplist = [u'在哪', u'哪儿', u'怎么走', u'怎么去', u'哪里']
    weblist = [u'网址', u'网页']
    txtlist = [u'通知', u'资料']
    piclist = [u'照片', u'相片', u'图片']
    if form.validate_on_submit():
        question = form.question.data
        keywords = jieba.analyse.extract_tags(question,10)
        psegword = pseg.cut(question)
        tag = 'unk'
        for i in psegword:
            keydict[i.word] = i.flag
        for i in keywords:
            if i in weblist:
                tag = 'web'
                del keydict[i]
                for j in keydict:
                    if j.flag == 'ns' or j.flag == 'nt' or j.flag == 'n' or j.flag == 'x':
                        keyword = j.word
                        break
            elif i in piclist:
                tag = 'pic'
                del keydict[i]
                for j in keydict:
                    if j.flag == 'ns' or j.flag == 'nt' or j.flag == 'n' or j.flag == 'x':
                        keyword = j.word
                        break
            elif i in maplist:
                tag = 'map'
                del keydict[i]
                for j in psegword:
                    if j.flag == 'ns' or j.flag == 'nt'  or j.flag == 'n'or j.flag == 'x':
                        keyword = j.word
                        break
            elif i in txtlist:
                tag = 'txt'
                for j in psegword:
                    if j.flag == 'ns' or j.flag == 'nt'  or j.flag == 'n'or j.flag == 'x':
                        keyword = j.word
                        break
            else:
                tag = 'unk'
        form.question.data = ''
    return render_template('index.html', form=form, question=question, tag=tag, keyword=keyword)
