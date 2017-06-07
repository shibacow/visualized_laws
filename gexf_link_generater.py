#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
sys.path.append('lib')
import yaml
import networkx as nx
import mog_op
from law_info import ChangeWareki
import logging
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")
import colorsys
import re
import time
from datetime import datetime

config=yaml.load(open('config/config.yaml'))
class LinkCheck(object):
    def __init__(self,mp):
        self.mp=mp
    def __target_color__(self,target_dict,title,cat):
        target_dict[title]=cat
    def __conv_color__(self,cofig):
        color_dict={}
        for c in config['COLORS']:
            t=config['COLORS'][c]
            h=t['h']
            s=t['s']
            v=t['b']
            k=colorsys.hsv_to_rgb(h,s,v)
            color_dict[c]={'r':int(k[0]*255),'g':int(k[1]*255),'b':int(k[2]*255)}
        return color_dict
    def __strip_title(self,tl):
        t=re.split(u"（",tl)[0]
        return t
    def generate(self,cat):
        graph = nx.DiGraph()
        edges=set()
        target_colors={}
        color_dict=self.__conv_color__(config)
        for k in self.mp.link.find({"src_cat":cat["_id"]}):
            src=k['src_title']
            dst=k['dst_title']
            self.__target_color__(target_colors,src,k['src_cat'])
            self.__target_color__(target_colors,dst,k['dst_cat'])
            edges.add((src,dst))
        graph.add_edges_from(edges)
        degree=nx.degree(graph)
        for n in graph.nodes(data=False):
            ch=ChangeWareki(n)
            result=ch.conv_date(n)
            #ch.conv_go(n)
            info=ch.get_info()
            deg=degree[n]
            cat_color=target_colors[n]
            color=color_dict[cat_color]
            if result:
                graph.node[n]['viz']={'size':deg,'color':color}
                dt=info["created_date"]
                sft="{0}-{1:02d}-{2:02d}".format(dt.year,dt.month,dt.day)
                end="2017-06-06"
                graph.node[n]['start']=sft
                graph.node[n]['end']=end
                graph.node[n]['label']=self.__strip_title(n)
        nx.write_gexf(graph,u"out_gexf/gexf_{}.gexf".format(cat["_id"]))
    def groupby_cat(self):
        return self.mp.groupby_cat('base')

def main():
    mp=mog_op.MongoOp('localhost')
    lc=LinkCheck(mp)
    catlist=lc.groupby_cat()
    for i,c in enumerate(catlist):
        lc.generate(c)
if __name__=='__main__':main()
