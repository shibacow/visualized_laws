#!/usr/bin/python
# -*- coding:utf-8 -*-
import pymongo
class MongoOp(object):
    def __init__(self,host):
        self.con=pymongo.Connection(host,27017)
        self.db=self.con.laws
        self.law_base=self.db.base
    def save(self,db,a):
        if a:
            if not self.db[db].find({'hash':a['hash']}):
                self.db[db].insert(a)
            else:
                self.db[db].save(a)
