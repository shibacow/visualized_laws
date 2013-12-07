#!/usr/bin/python
# -*- coding:utf-8 -*-
import mog_op
from pyquery import PyQuery as pq
import re
from urlparse import urljoin
from bson.objectid import ObjectId

src='http://law.e-gov.go.jp/'
class LinkCheck(object):
    def __init__(self,mp):
        self.mp=mp
    def pickup_link(self,l,d):
        chset=set()
        for a in d('a'):
            ad=pq(a)
            href=ad.attr.href
            if href and re.search('^/cgi-bin/idxrefer.cgi',href):
                url=urljoin(src,href)
                child=self.mp.ref.find_one({"url":url})
                if child:
                    #l['_id']
                    child['parent']=ObjectId(l['_id'])
                    chset.add(ObjectId(child['_id']))
                    self.mp.save_data('ref_title',child)
                child=None
        chlist=[c for c in chset]
        csize=len(chlist)
        l['children']=chlist
        self.mp.save_data('base',l)
        chlist=None
        return csize
    def split_law_name(self):
        for i,l in enumerate(self.mp.law_base.find()):
            body=l['body']
            body=pq(body)
            csize=self.pickup_link(l,body)
            print i,csize,l['title']
            l=None
            
def main():
    mp=mog_op.MongoOp('localhost')
    lc=LinkCheck(mp)
    lc.split_law_name()
    
if __name__=='__main__':main()
