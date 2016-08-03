# coding: utf-8
from . import app, db
from flask import Flask
from flask import jsonify
import jieba
import jieba.analyse
import jieba.posseg as pseg
jieba.load_userdict("dic.txt")


@app.route('/<text>', methods=['GET','POST'])
def index(text):
    tag = 'unk'
    keyword = None
    content = None
    keydict = {}
    adict = {}
    maplist = [u'在哪', u'哪儿', u'怎么走', u'怎么去', u'哪里', u'地图']
    weblist = [u'网址', u'网页', u'网站']
    txtlist = [u'通知', u'资料', u'公告']
    piclist = [u'照片', u'相片', u'图片']
    keywords = jieba.analyse.extract_tags(text,10)
    psegword = pseg.cut(text)
    for n in psegword:
        keydict[n.word] = n.flag
    for i in keywords:
        if i in weblist:
            del keydict[i]
            for j in keydict:
                if keydict[j] == 'ns' or keydict[j] == 'nt' or keydict[j] == 'n' or keydict[j] == 'x':
                    keyword = j
                    adict = db.web.find({'index':keyword})
            for k in adict:
                tag = k['tag']
                index = k['index']
                content = k['content']
                return jsonify({
                    'tag':tag,
                    'content':content
                })
        elif i in piclist:
            del keydict[i]
            for j in keydict:
                if keydict[j] == 'ns' or keydict[j] == 'nt' or keydict[j] == 'n' or keydict[j] == 'x':
                    keyword = j
                    adict = db.pic.find({'index': keyword})
            for k in adict:
                tag = k['tag']
                index = k['index']
                content = k['content']
                return jsonify({
                    'tag':tag,
                    'content':content
                })
        elif i in maplist:
            tag = 'map'
            for j in keydict:
                if keydict[j] == 'ns' or keydict[j] == 'nt'  or keydict[j] == 'n'or keydict[j] == 'x':
                    keyword = j
                    content = keyword
                    return jsonify({
                        'tag':tag,
                        'content':content
                    })
        elif i in txtlist:
            for j in keydict:
                if keydict[j] == 'ns' or keydict[j] == 'nt'  or keydict[j] == 'n'or keydict[j] == 'x':
                    keyword = j
                    adict = db.txt.find({'index': keyword})
            for k in adict:
                tag = k['tag']
                index = k['index']
                content = k['content']
                return jsonify({
                    'tag':tag,
                    'content':content
                })
        else:
            tag = 'unk'
            content = None
    return jsonify({
            'tag':'unk',
            'content':None
        })
