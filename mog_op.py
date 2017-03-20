#!/usr/bin/python
# -*- coding:utf-8 -*-
import pymongo
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
MONGO_DB=os.environ.get("MONGO_DB")

class NewMongoOp(object):
    def __init__(self,host):
        self.con=pymongo.MongoClient(host,27017)
        self.db=self.con[MONGO_DB]
        self.col=self.db.laws
    def insert(self,dkt):
        title=dkt['title']
        if not self.col.find_one({title:title}):
            self.col.insert_one(dkt)
    def has_one(self,title):
        return self.col.find_one({title:title})

class MongoOp(object):
    def __init__(self,host):
        self.con=pymongo.MongoClient(host,27017)
        self.db=self.con.laws
        self.law_base=self.db.base
        self.ref=self.db.ref_title
        self.link=self.db.link

    def save(self,db,a,key):
        if a:
            if not self.db[db].find_one({key:a[key]}):
                self.db[db].insert(a)
            else:
                self.db[db].save(a)
    def save_link(self,a):
        if not self.link.find_one({"src_id":a['src_id'],
                                   "link_id":a['link_id'],
                                   "dst_id":a['dst_id']}):
            self.link.insert(a)
            #print 'insert law=%s' % a['src_title']
    def save_data(self,db,a):
        if a:
            dbm=getattr(self.db,db)
            ##self.db[db].save(a)
            dbm.save(a)
    def groupby_cat(self,col,tdict):
        return self.db[col].group(tdict,None,{},'function(obj,prev){}')
