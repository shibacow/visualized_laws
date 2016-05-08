#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask,render_template
import os
from glob import glob
import random

app = Flask(__name__)
gexfdir=os.getcwd()+"/static/gexf/*.gexf"
gexfs=glob(gexfdir)

class Gexf(object):
    def __init__(self,g,basedir):
        self.gpath=unicode(g,'utf-8')
        self.gexfpath=os.path.relpath(self.gpath,basedir)
        cat=os.path.basename(self.gpath)
        cat=cat.split('.')[0]
        self.cat=cat

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/all')
def all():
    basedir=os.getcwd()
    gexf=[Gexf(g,basedir) for g in gexfs]
    random.shuffle(gexf)
    return render_template("all.html",gexfs=gexf[:4])

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

