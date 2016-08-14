# -*- coding: utf-8 -*-


import os
from . import auth
from .. import db
from flask import render_template, request, flash, redirect, url_for


@auth.route('/')
def index():
    collections = db.collection_names()
    return render_template('index.html', collections=collections)


@auth.route('/showcollection/')
def showcollection():
    collection_name = request.args.get('collection')
    collection = db.get_collection(collection_name)
    adict = collection.find()
    if adict.count():
        name = collection_name
        return render_template('showcollection.html',
                adict=adict,
                name=name
                )
    else:
        return 'No Available Data!'


@auth.route('/addinfo/', methods=['GET', 'POST'])
def addinfo():
    collections = db.collection_names()
    if request.method == 'POST':
        in_tag = request.form.get('tag')
        in_index = request.form.get('index')
        in_content = request.form.get('content')
        if (in_tag and in_index and in_content):
            db.get_collection(in_tag).insert({
                        'tag': in_tag,
                        'index': in_index,
                        'content': in_content
                        })
            flash("Data has been inserted!")
        else:
            flash("Please complete the blanks!")
        return redirect(url_for('auth.addinfo'))
    return render_template('addinfo.html', collections=collections)


@auth.route('/rminfo/', methods=['GET', 'POST'])
def rminfo():
    collections = db.collection_names()
    if request.method == 'POST':
        rm_tag = request.form.get('tag')
        rm_index = request.form.get('index')
        rm_content = request.form.get('content')
        if (rm_tag and rm_tag and rm_content):
            db.get_collection(rm_tag).delete_one({
                'tag': rm_tag,
                'index': rm_index,
                'content': rm_content
                })
            flash("Data has been deleted!")
        else:
            flash("Please complete the blanks!")
        return redirect(url_for('auth.rminfo'))
    return render_template('rminfo.html', collections=collections)


@auth.route('/rmcollection/', methods=['GET', 'POST'])
def rmcollection():
    collections = db.collection_names()
    if request.method == 'POST':
        rm_collection = request.form.get('rm_collection')
        if rm_collection:
            db.get_collection(rm_collection).drop()
            flash("Collection has been dropped!")
        else:
            flash("Please complete the blanks!")
        return redirect(url_for('auth.rmcollection'))
    return render_template('rmcollection.html', collections=collections)

@auth.route('/addtodic/', methods=['GET', 'POST'])
def addtodic():
    if request.method == 'POST':
        words = request.form.get('words')
        types = request.form.get('types')
        if words and types:
            route = os.getcwd()+'/dic.txt'
            with open(route, 'at') as f:
                f.write(words + ' ' + types + '\n')
            flash("Words has been added!")
        else:
            flash("Please complete the blanks!")
        return redirect(url_for('auth.addtodic'))
    return render_template('addtodic.html')
