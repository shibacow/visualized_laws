#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('lib')
#import networkx as nx
from mog_op import NewMongoOp
from glob import glob
import unicodecsv
import simstring
import xml.etree.ElementTree as ET
import logging
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")
import re
import os

def read_csv():
    law_dict={}
    r=unicodecsv.reader(open('abbreviation.csv','rb'),encoding='utf-8')
    for row in r:
        k=row[0]
        law_dict[k]=[c for c in row if c!='']
    return law_dict

def get_mp_data(mp,law_dict):
    col=mp.con['laws_2018-09-24'].raw_laws
    dkt={}
    for a in col.find({},{'title':1,'href':1}):
        #logging.info(u"title={} url={}".format(a['title'],a['href']))
        dkt[a['title']]=a['href']
        for kk in law_dict.get(a['title'],[]):
            #logging.info(kk)
            if isinstance(kk,str):
                kk=unicode(kk,'utf-8')
            dkt[kk]=a['href']
    return dkt
def write_simstring(dkt):
    dbpath='simstring_law/law.db'
    db=simstring.writer(dbpath,3,False,True)
    for k in dkt:
        if isinstance(k,unicode):
            k=k.encode('utf-8')
        db.insert(k)
def read_simstring():
    dbpath='simstring_law/law.db'
    db=simstring.reader(dbpath)
    db.measure = simstring.cosine
    db.threshold=0.9
    return db

def read_xml(f,dkt2):
    logging.info("read={}".format(f))
    tree = ET.ElementTree(file=f)
    root = tree.getroot()
    xpath=".//{http://www.gexf.net/1.3}node"
    for n in root.findall(xpath):
        label=n.get('label')
        if isinstance(label,str):
            label=unicode(label,'utf-8')
        for attr in n.getiterator("{http://www.gexf.net/1.3}attvalue"):
            if attr.get('for')=='url':
                url=attr.get('value')
                dkt2[label]=url
def write_xml(f,url_match):
    logging.info("write={}".format(f))
    tree = ET.ElementTree(file=f)
    root = tree.getroot()
    xpath=".//{http://www.gexf.net/1.3}node"
    ET.register_namespace('', 'http://www.gexf.net/1.3')
    ET.register_namespace('viz', 'http://www.gexf.net/1.3/viz')
    for n in root.findall(xpath):
        label=n.get('label')
        if isinstance(label,str):
            label=unicode(label,'utf-8')
        for attr in n.getiterator("{http://www.gexf.net/1.3}attvalue"):
            if attr.get('for')=='url':
                url=url_match.get(label,None)
                if url:
                    attr.set('value',url)
                    #logging.info(url)
                    #pass
    outf="temp_xml/{}".format(os.path.basename(f))
    logging.info(outf)
    tree.write(outf,encoding='utf-8')

def combine(dkt,dkt2,db):
    not_match=[]
    url_match={}
    for k in dkt2:
        v0=dkt2[k]
        v1=dkt.get(k,None)
        if not v1:
            korg=k
            #logging.info(u'k={}'.format(k))
            if isinstance(k,unicode):
                k=k.encode('utf-8')
            is_match=False
            for a in db.retrieve(k):
                #logging.info("\tk={}\tr={}".format(k,a))
                is_match=True
                v1=dkt.get(a)
            if not is_match:
                not_match.append(korg)
        if v1:
            #logging.info(u"v0={} v1={}".format(v0,v1))
            if v0:
                assert(re.search('http://law\.e-gov',v0))
            else:
                logging.info(u'k={}'.format(k))
            if v1:
                assert(re.search('http://elaws\.e-gov',v1))
            url_match[k]=v1
           
    logging.info(len(not_match))
    #for a in not_match:
    #    logging.info(u"not_match={}".format(a))
    logging.info(len(not_match))
    return url_match
def modify_link():
    mp=NewMongoOp()
    law_dict=read_csv()
    dkt=get_mp_data(mp,law_dict)
    #write_simstring(dkt)
    db=read_simstring()
    gd='../visualized_laws_web/app/data/kenpo.gexf'
    gd='../visualized_laws_web/app/data/*.gexf'
    dkt2={}
    for f in list(glob(gd)):
        read_xml(f,dkt2)
    url_match=combine(dkt,dkt2,db)
    for f in glob(gd):
        write_xml(f,url_match)

class ImgSize(object):
    def __init__(self,label,f):
        self.f=f
        self.label=label
        self.u0=None
        self.size=0
    def __str__(self):
        return u"file={} l={} u0={} size={}".\
            format(self.f,self.label,self.u0,self.size)
        
def write_alone(f):
    #logging.info("write={}".format(f))
    tree = ET.ElementTree(file=f)
    root = tree.getroot()
    xpath=".//{http://www.gexf.net/1.3}node"
    ET.register_namespace('', 'http://www.gexf.net/1.3')
    ET.register_namespace('viz', 'http://www.gexf.net/1.3/viz')
    for n in root.findall(xpath):
        label=n.get('label')
        img=ImgSize(label,f)
        if isinstance(label,str):
            label=unicode(label,'utf-8')
        for attr in n.getiterator("{http://www.gexf.net/1.3}attvalue"):
            if attr.get('for')=='url':
                u0=attr.get('value')
                if re.search('http://law\.e-gov\.go.jp/',u0):
                    img.u0=u0
        size=n.getiterator("{http://www.gexf.net/1.3/viz}size")
        size=size[0].get('value')
        if size:
            size=int(float(size))
            img.size=size
        if img.u0 and img.size> 30:
            logging.info(u'img={}'.format(img))

def gleaning():
    gd='../visualized_laws_web/app/data/*.gexf'
    for f in glob(gd):
        write_alone(f)
    
def main():
    gleaning()
if __name__=='__main__':main()
