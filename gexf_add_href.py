#!/usr/bin/env python
# -*- coding:utf-8 -*-


import sys
sys.path.append('lib')
#import networkx as nx
from mog_op import NewMongoOp
from gexf import Gexf,GexfImport
from glob import glob
import logging
import unicodecsv
import xml.etree.ElementTree as ET
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")


def readcsv():
    law_dict={}
    r=unicodecsv.reader(open('abbreviation.csv','rb'),encoding='utf-8')
    for row in r:
        k=row[0]
        rr=[(len(a),a) for a in row[1:] if a]
        rr=sorted(rr,key=lambda x:x[0],reverse=False)
        law_dict[k]=rr[0][1]
    return law_dict

def importGraph(f,mp,law_dict):
    dst=f.split('/')[-1]
    g_import=Gexf.importXML(open(f))
    graph=g_import.graphs[0]
    graph.addNodeAttribute('URI',defaultValue="",type='string',force_id='URI')
    for node_id,node in graph.nodes.iteritems():
        regbase=u"^{}（".format(node.label)
        attr=node.getAttributes()
        logging.info(attr)
        if law_dict.has_key(node.label):
            v=law_dict[node.label]
            logging.info("v={}".format(v.encode('utf-8')))
        ab_law=law_dict.get(node.label,node.label)
        tt=mp.col.find({"title":{"$regex":regbase}})
        sz=tt.count()
        blink=''
        if sz==1:
            blink=tt[0]['body_link']
        #node.addAttribute("URI",blink)
        node.label=ab_law
    #dstf="addurl2/"+dst
    #g_import.write(open(dstf,'wb'))
def modifyxml(f,law_dict,mp):
    dst=f.split('/')[-1]
    tree = ET.parse(f)
    ET.register_namespace('','http://www.gexf.net/1.3')
    ET.register_namespace('viz','http://www.gexf.net/1.3/viz')

    root = tree.getroot()
    #for e in root.getiterator():
    #    logging.info(e.tag)
    for n in root.findall(".//{http://www.gexf.net/1.3}node"):
        n.attrib['url']=''
        if not 'label' in n.attrib:
            logging.info(n.attrib)
            continue
        label=n.attrib['label']
        regbase=u"^{}（".format(label)
        tt=mp.col.find({"title":{"$regex":regbase}})
        sz=tt.count()
        blink=''
        if sz==1:
            blink=tt[0]['body_link']
        #if law_dict.has_key(label):
        #    v=law_dict[label]
            #logging.info("v={}".format(v.encode('utf-8')))
        ab_law=law_dict.get(label,label)
        n.attrib['label']=ab_law
        n.attrib['url']=blink
    dstf="addurl2/"+dst
    tree.write(dstf,'UTF-8',True)
    
def main():
    law_dict=readcsv()
    mp=NewMongoOp('localhost')
    for f in list(glob("gexfall/*.gexf")):
        logging.info(f)
        modifyxml(f,law_dict,mp)

if __name__=='__main__':main()
