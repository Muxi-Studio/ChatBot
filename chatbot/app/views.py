# coding: utf-8
from . import app, db
from flask import render_template, redirect, flash, url_for, request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/addinfo/', methods=['GET', 'POST'])
def addinfo():
    if request.method == 'POST':
        in_tag = request.form.get('tag')
        in_index = request.form.get('index')
        in_content = request.form.get('content')
        if (in_tag and in_index and in_content):
            if in_tag == 'txt':
                db.txt.insert({'tag': in_tag, 'index': in_index, 'content': in_content})
            elif in_tag == 'pic':
                db.pic.insert({tag: in_tag, index: in_index, url: in_content})
            elif in_tag == 'web':
                db.web.insert({tag: in_tag, index: in_index, url: in_content})
            flash("数据已导入!")
        else:
            flash("输入完整信息!")
        return redirect(url_for('addinfo'))
    return render_template('addinfo.html')

@app.route('/showtxt/')
def showtxt():
    adict = db.txt.find()
    if adict.count():
        name = 'txt'
        return render_template('showdb.html', adict=adict, name=name)
    else:
        return '暂时没有数据...'

@app.route('/showpic/')
def showpic():
    adict = db.pic.find()
    if adict.count():
        name = 'pic'
        return render_template('showdb.html', adict=adict, name=name)
    else:
        return '暂时没有数据...'

@app.route('/showweb/')
def showweb():
    adict = db.web.find()
    if adict.count():
        name = 'web'
        return render_template('showdb.html', adict=adict, name=name)
    else:
        return '暂时没有数据...'
