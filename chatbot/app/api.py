
# coding: utf-8
from . import app, db
from .replace import replace_word
from flask import request, jsonify, redirect, url_for
import re
import jieba
import jieba.analyse
import jieba.posseg
import urllib2
import urllib
import json
import random
from collections import OrderedDict
jieba.load_userdict("dic.txt")

@app.route('/<text>', methods=['GET','POST'])
def getcontent(text):
    text = text.decode("utf8")
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),text)
    questionlist = []
    if request.method == 'GET':
        questions = db.question.find({'content':text})
        for n in questions:
            questionlist.append(n)
        if questionlist == []:
            db.question.insert({'tag':'question','index': 'question','content': text})
    maplist = [u'在哪', u'哪儿', u'哪里', u'地图', u'怎么走', u'怎么去']
    weblist = [u'网址', u'网页', u'网站', u'官网']
    txtlist = [u'通知', u'资料', u'公告']
    piclist = [u'照片', u'相片', u'图片']
    tag = None
    keyword = None
    content = None
    a = {}
    alist = []
    adict = {}
    keydict = OrderedDict()
    text = replace_word(text)
    keywords = jieba.analyse.extract_tags(text,10)
    psegwords = jieba.posseg.cut(text)
    for psegword in psegwords:
        keydict[psegword.word] = psegword.flag
    if keywords != []:
        for i in weblist:
            if i in keywords:
                tag = 'web'
                del keydict[i]
                for j in keydict:
                    keyword = j
                    a = db.web.find({'index':keyword})
                    alist = [m for m in a]
                    if alist != []:
                        adict = random.choice(alist)
                        tag = adict['tag']
                        content = adict['content']
                        return jsonify({
                            'tag':tag,
                            'content':content
                        })
        for i in piclist:
            if i in keywords:
                tag = 'pic'
                del keydict[i]
                for j in keydict:
                    keyword = j
                    a = db.pic.find({'index': keyword})
                    alist = [m for m in a]
                    if alist != []:
                        adict = random.choice(alist)
                        tag = adict['tag']
                        content = adict['content']
                        return jsonify({
                            'tag':tag,
                            'content':content
                        })
        for i in maplist:
            if i in keywords:
                tag = 'map'
                for j in keydict:
                    if keydict[j] == 'ns' or keydict[j] == 'nt'  or keydict[j] == 'n' or keydict[j] == 'nr':
                        keyword = j
                        content = keyword
                return jsonify({
                    'tag':tag,
                    'content':content
                })
        for i in txtlist:
            tag = 'txt'
            if i in keywords:
                del keydict[i]
            for j in keydict:
                keyword = j
                a = db.txt.find({'index': keyword})
                alist = [m for m in a]
                if alist != []:
                    adict = random.choice(alist)
                    tag = adict['tag']
                    content = adict['content']
                    return jsonify({
                        'tag':tag,
                        'content':content
                    })
    a = db.txt.find({'index': text})
    alist = [m for m in a]
    if alist != []:
        adict = random.choice(alist)
        tag = adict['tag']
        content = adict['content']
        return jsonify({
            'tag':tag,
            'content':content
        })
    return chat(text) 

@app.route('/chat/<text>', methods=['GET', 'POST'])
def chat(text):
    text = urllib.quote(text.encode('utf8'))
    url = 'http://www.tuling123.com/openapi/api?key=05f603714dd44697b554e31d152c1118&info=' + text
    dictHtml = urllib.urlopen(url)
    dictHtml1 = dictHtml.read()
    dictJSON = json.loads(dictHtml1)
    content = dictJSON['text']
    tag = 'txt'
    return jsonify({
        'tag':tag,
        'content':content
    })  