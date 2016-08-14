# coding: utf-8
from . import app, db
from flask import Flask, jsonify, redirect, url_for
import re
import jieba
import jieba.analyse
import jieba.posseg
jieba.load_userdict("dic.txt")
import urllib2
import urllib
import json

@app.route('/<text>', methods=['GET','POST'])
def getcontent(text):
    tag = 'unk'
    keyword = None
    content = None
    keydict = {}
    adict = {}
    maplist = [u'在哪', u'哪儿', u'哪里', u'地图']
    weblist = [u'网址', u'网页', u'网站']
    txtlist = [u'通知', u'资料', u'公告']
    piclist = [u'照片', u'相片', u'图片']
    text = text.decode("utf8")
    text = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),text)
    keywords = jieba.analyse.extract_tags(text,10)
    psegword = jieba.posseg.cut(text)
    for n in psegword:
        keydict[n.word] = n.flag
    if keywords != []:
        for i in weblist:
            if i in keywords:
                tag = 'web'
                del keydict[i]
                for j in keydict:
                    if keydict[j] == 'ns' or keydict[j] == 'nt' or keydict[j] == 'n' or keydict[j] == 'nr':
                        keyword = j
                        adict = db.web.find({'index':keyword})
                        break
                for k in adict:
                    tag = k['tag']
                    content = k['content']
                    return jsonify({
                        'tag':tag,
                        'content':content
                    })
        for i in piclist:
            if i in keywords:
                tag = 'pic'
                del keydict[i]
                for j in keydict:
                    if keydict[j] == 'ns' or keydict[j] == 'nt' or keydict[j] == 'n' or keydict[j] == 'nr':
                        keyword = j
                        adict = db.pic.find({'index': keyword})
                        break
                for k in adict:
                    tag = k['tag']
                    content = k['content']
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
                if keydict[j] == 'ns' or keydict[j] == 'nt'  or keydict[j] == 'n' or keydict[j] == 'nr':
                    keyword = j
                    adict = db.txt.find({'index': keyword})
                    break
            for k in adict:
                tag = k['tag']
                content = k['content']
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