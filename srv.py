#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask,render_template
import os
from glob import glob
app = Flask(__name__)
gexfdir=os.getcwd()+"/static/gexf/*.gexf"
gexfs=glob(gexfdir)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/all')
def all():
    basedir=os.getcwd()
    gexf=[os.path.relpath(unicode(g,'utf-8'),basedir) for g in gexfs]
    return render_template("all.html",gexfs=gexf)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

    
