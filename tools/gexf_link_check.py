#!/usr/bin/python
# -*- coding:utf-8 -*-
# gexfのidで指定した法律IDで実際のlaw.baseのtitleをマッチさせて、ログが取れるかの確認

import sys
sys.path.append('../lib')
import networkx as nx
from mog_op import MongoOp
import logging
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")
from glob import glob

def parse(graph,mp):
    for n in graph.nodes(data=True):
        t=n[0]
        c=mp.law_base.find_one({'title':t})
        if not c:
             assert(False)
def main():
    mp=MongoOp('localhost')
    for f in glob("../out_gexf/*.gexf"):
        print(f)
        graph=nx.read_gexf(f)
        parse(graph,mp)
if __name__=='__main__':main()
