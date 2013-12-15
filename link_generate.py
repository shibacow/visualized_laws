#!/usr/bin/python
# -*- coding:utf-8 -*-
import mog_op
from pyquery import PyQuery as pq
import re
from urlparse import urljoin
from bson.objectid import ObjectId
import csv
import logging
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")


class LinkCheck(object):
    def __init__(self,mp):
        self.mp=mp

    def __lspliter(self,s):
        cc=s.split(u'（')
        if len(cc)>3:
            cc=cc[1:]
        if len(cc)>1:
            return cc[0]
        else:
            return []
    def write_csv(self,cname,clist):
        cout=csv.writer(open(cname,'ab'))
        cout.writerows(clist)
    
    def cat_collect(self,cat):
        nodeset=set()
        srcdict={}
        for k in self.mp.link.find({"src_cat":cat}):
            dst=self.__lspliter(k['dst_title'])
            src=self.__lspliter(k['src_title'])
            if dst and src:
                srcdict.setdefault(src,{})
                srcdict[src].setdefault(dst,0)
                srcdict[src][dst]+=1
                nodeset.add(src)
                nodeset.add(dst)
        edges_filename=cat+'_edges.csv'
        node_filename=cat+'_node.csv'
        self.write_csv(edges_filename,[['source','target']])
        for a,b in srcdict.items():
            clist=[]
            for c,d in b.items():
                clist.append((a.encode('utf-8'),c.encode('utf-8')))
            self.write_csv(edges_filename,clist)
        nodelist=[('Id','Label')]
        for n in nodeset:
            nn=n.encode('utf-8')
            nodelist.append((nn,nn))
        self.write_csv(node_filename,nodelist)
                
def main():
    mp=mog_op.MongoOp('localhost')
    lc=LinkCheck(mp)
    lc.cat_collect(u"海運")

if __name__=='__main__':main()
