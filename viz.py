#!/usr/bin/python
# -*- coding:utf-8 -*-
from glob import glob
import os
import re
from pyquery import PyQuery as pq
from urllib import unquote
import bz2
import mog_op
from datetime import datetime

basedir='../law.e-gov.go.jp/data2'

class LawCat(object):
    def __init__(self,sha,title,cat):
        self.sha=sha
        self.title=unicode(title,'utf-8')
        self.cat=unicode(cat,'utf-8')
    def __str__(self):
        return "sha=%s title=%s cat=%s" % (self.sha,self.title.encode('utf-8'),self.cat.encode('utf-8'))

def downfile():
    ls={}
    for l in open(basedir+os.sep+'downloaded'):
        l=l.strip()
        l=re.sub('\n','',l)
        l2=l.split('\t')
        if len(l2)==3:
            ls[l2[0]]=LawCat(l2[0],l2[1],l2[2])
        else:
            pass
            #print "==%s==" % l
    return ls

def parsehref(href,dkt):
    if len(href.split('?'))!=2:
        return 
    tt=href.split('?')[1]
    for cc in tt.split('&'):
        (k,v)=cc.split('=')
        v=unquote(v)
        v=unicode(v,'cp932')
        print k,v
class Count(object):
    def __init__(self):
        self.cnt=0
        self.lcnt=0
    def inc(self):
        self.cnt+=1
    def linc(self):
        self.lcnt+=1
def pprint(r):
    d=pq(r)
    cnt.linc()
    for a in d('a'):
        ad=pq(a)
        href=ad.attr('href')
        txt=ad.text()
        if href:
            cnt.inc()
    
def parsedict(f,ldict,cnt,mp):
    bs=os.path.basename(f)
    bs=bs.split('.')[0]
    if bs in ldict:
        dkt=ldict[bs]
        r=open(f).read()
        r=unicode(r,'cp932')
        #bzaa=bz2.compress(r.encode('utf-8'))
        d={'title':dkt.title,'body':r,'cat':dkt.cat,\
               'hash':dkt.sha,'created_at':datetime.now()}
        mp.save('base',d)
        
        print dkt.cat,dkt.title
        print len(r)
    else:
        print 'not found'
def main():
    ls=downfile()
    cnt=Count()
    mp=mog_op.MongoOp('localhost')
    for f in glob(basedir+os.sep+'html/*.html'):
        parsedict(f,ls,cnt,mp)
        

if __name__ =='__main__':main()
