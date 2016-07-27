from flask import Flask
from . import app, db
from flask import jsonify


@app.route('/gettxt/<keyword>', methods=['GET', 'POST'])
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

@app.route('/getweb/<keyword>', methods=['GET', 'POST'])
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

@app.route('/getpic/<keyword>', methods=['GET', 'POST'])
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
        