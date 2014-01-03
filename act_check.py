#!/usr/bin/python
# -*- coding:utf-8 -*-
from mog_op import MongoOp
from bson.objectid import ObjectId

import time
import logging

logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")

class ActCheck(object):
    def __match(self,title):
        r=self.mp.law_base.find({"title":title})
        assert(r.count>0)
        for k in r:
            k['is_act']=True
            self.mp.law_base.save(k)

    def __init__(self,mp,actlist):
        self.mp=mp
        self.actlist=actlist
    def baseAttchAct(self):
        for c in actlist:
            self.__match(c)
    def linkCheck(self):
        for i,k in enumerate(self.mp.law_base.find({"is_act":True})):
            oid=ObjectId(k['_id'])
            #for l in mp.link.find({"src_id":oid}):
            #    print l
            src=self.mp.link.find({"src_id":oid})
            print "i=%d src count=%d"  % (i,src.count())
            for s in src:
                s['src_is_act']=True
                self.mp.link.save(s)

            dst=self.mp.link.find({"dst_id":oid})
            print "i=%d dst count=%d"  % (i,dst.count())
            for d in dst:
                d['dst_is_act']=True
                self.mp.link.save(d)

def readActList(fname):
    aclist=[]
    for l in open(fname).readlines():
        l=l.strip()
        l=unicode(l,'utf-8')
        aclist.append(l)
    return aclist
def main():
    aclist=readActList('act_list.txt')
    mp=MongoOp('localhost')
    ac=ActCheck(mp,aclist)
    #ac.linkCheck()
if __name__=='__main__':main()
