#!/usr/bin/python
# -*- coding:utf-8 -*-
import pymongo
class MongoOp(object):
    def __init__(self,host):
        self.con=pymongo.Connection(host,27017)
        self.db=self.con.laws
        self.law_base=self.db.base
        self.ref=self.db.ref_title

    def save(self,db,a,key):
        if a:
            if not self.db[db].find_one({key:a[key]}):
                self.db[db].insert(a)
            else:
                self.db[db].save(a)
