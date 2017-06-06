#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append('lib')
import networkx as nx
import mog_op
import law_info
import logging
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")

class LinkCheck(object):
    def __init__(self,mp):
        self.mp=mp

    def generate(self,cat):
        graph = nx.DiGraph()
        edges=set()
        for k in self.mp.link.find({"src_cat":cat["_id"]}):
            src=k['src_title']
            dst=k['dst_title']
            edges.add((src,dst))
        graph.add_edges_from(edges)
        degree=nx.degree(graph)
        for n in graph.nodes(data=False):
            deg=degree[n]
            if deg > 100:
                print(u"deg={} n={}".format(deg,n))
    def groupby_cat(self):
        return self.mp.groupby_cat('base')

def main():
    mp=mog_op.MongoOp('localhost')
    lc=LinkCheck(mp)
    catlist=lc.groupby_cat()
    for i,c in enumerate(catlist):
        lc.generate(c)
if __name__=='__main__':main()
