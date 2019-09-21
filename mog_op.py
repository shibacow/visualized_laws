#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
import re
MONGO_HOST=os.environ.get("MONGO_HOST")
MONGO_USER=os.environ.get("MONGO_USER")
PASSWORD=os.environ.get("PASSWORD")
AUTHSOURCE=os.environ.get("AUTHSOURCE")

class MongoOp(object):
    def __init__(self):
        self.con = pymongo.MongoClient(MONGO_HOST,
                                       27017,
                                       username=MONGO_USER,
                                       password=PASSWORD,
                                       authSource=AUTHSOURCE,
                                       authMechanism='SCRAM-SHA-1')
    def get_collections(self,db_name):
        db=self.con[db_name]
        for c in db.list_collections():
            cname=c['name']
            print(u'db={} cname={}'.format(db_name,cname))
            
    def get_col(self,db_name,c_name):
        return self.con[db_name][c_name]
    
    def __del__(self):
        if self.con:
            self.con.close()
            self.con=None
    def close(self):
        if self.con:
            self.con.close()
            self.con=None
def get_dt():
    mp=MongoOp()
    #print(dir(mp.con))
    for db in mp.con.list_databases():
        nm=db['name']
        if re.search('law',nm):
            #print(nm)
            mp.get_collections(nm)
def get_raw_percedent():
    db='laws_2018-03-04'
    col='raw_percedent'
    mp=MongoOp()
    col = mp.get_col(db,col)
    for a in col.find({}).limit(100):
        #print(a.keys())
        if 'main_text' in a:
            mt = a['main_text']
            print(len(mt))
            print(mt)
if __name__=='__main__':get_raw_percedent()



