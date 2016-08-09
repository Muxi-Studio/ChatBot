#coding: utf-8
from . import app, db
from flask import Flask, jsonify
import re
import jieba
import jieba.analyse
import jieba.posseg
jieba.load_userdict("dic.txt")


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
            if adict == {}:
                adict = db.txt.find({'index': text})
            for k in adict:
                tag = k['tag']
                content = k['content']
                return jsonify({
                    'tag':tag,
                    'content':content
                })
    if keywords == []:
        adict = db.txt.find({'index': text})
        for k in adict:
            tag = k['tag']
            content = k['content']
            return jsonify({
                'tag':tag,
                'content':content
            })
    return jsonify({
        'tag':'unk',
        'content':None
    })