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
class ModifyXML(object):
    def __modify_label(self,root):
        for n in root.findall(".//{http://www.gexf.net/1.3}node"):
            if not 'label' in n.attrib:
                logging.info(n.attrib)
                continue
            label=n.attrib['label']
            ab_law=self.law_dict.get(label,label)
            n.attrib['label']=ab_law
    def __add_meta(self,root):
        attr=root.find(".//{http://www.gexf.net/1.3}attributes")
        alt=ET.Element("attribute",{"id":"url","title":"url","type":"string"})
        attr.append(alt)
    def __modify_url(self,root):
        for n in root.findall(".//{http://www.gexf.net/1.3}node"):
            if not 'label' in n.attrib:
                logging.info(n.attrib)
                continue
            label=n.attrib['label']
            regbase=u"^{}（".format(label)
            tt=self.mp.col.find({"title":{"$regex":regbase}})
            sz=tt.count()
            blink=''
            if sz==1:
                blink=tt[0]['body_link']
            attrs=n.find("{http://www.gexf.net/1.3}attvalues")
            #logging.info(attrs)
            elm=ET.Element("attvalue",{"for":"url","value":blink})
            attrs.append(elm)

    def save(self):
        dstf="addurl2/"+self.dst
        self.tree.write(dstf,'UTF-8',True)
    def modify(self):
        self.__add_meta(self.root)
        self.__modify_url(self.root)
        self.__modify_label(self.root)
    def __init__(self,f,law_dict,mp):
        self.mp=mp
        self.law_dict=law_dict
        self.dst=f.split('/')[-1]
        self.tree = ET.parse(f)
        ET.register_namespace('','http://www.gexf.net/1.3')
        ET.register_namespace('viz','http://www.gexf.net/1.3/viz')

        self.root = self.tree.getroot()
    def show(self):
        for e in self.root.getiterator():
            logging.info(e.tag)

def modifyxml(f,law_dict,mp):
    mx=ModifyXML(f,law_dict,mp)
    mx.modify()
    #mx.show()
    mx.save()
def main():
    law_dict=readcsv()
    mp=NewMongoOp('localhost')
    for f in list(glob("gexfall/*.gexf")):
        logging.info(f)
        modifyxml(f,law_dict,mp)

if __name__=='__main__':main()
