#!/usr/bin/python
# -*- coding:utf-8 -*-
import mog_op
from pyquery import PyQuery as pq
import re
from urlparse import urljoin
from bson.objectid import ObjectId
import csv
import logging
import re
import os
from glob import glob

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
    def cat_collect(self,src_cat):
        d=dict(src_cat=src_cat)
        self.__collect(d,prefix=src_cat)
    def act_collect(self):
        d=dict(src_is_act=True,dst_is_act=True)
        self.__collect(d,"is_act",'actcsv')
    def __collect(self,conddict,prefix="default",csvdir="csvdir"):
        nodeset=set()
        srcdict={}
        nodedict={}
        dstcat={}
        for k in self.mp.link.find(conddict):
            dst=self.__lspliter(k['dst_title'])
            src=self.__lspliter(k['src_title'])
            dstcat[dst]=k['dst_cat']
            if dst and src:
                srcdict.setdefault(src,{})
                srcdict[src].setdefault(dst,0)
                srcdict[src][dst]+=1
                nodeset.add(src)
                nodeset.add(dst)
                nodedict.setdefault(src,0)
                nodedict[src]+=1
        edges_filename=csvdir+os.sep+prefix+'_edges.csv'
        node_filename=csvdir+os.sep+prefix+'_node.csv'
        self.write_csv(edges_filename,[['source','target']])
        for a,b in srcdict.items():
            clist=[]
            for c,d in b.items():
                clist.append((a.encode('utf-8'),c.encode('utf-8')))
            self.write_csv(edges_filename,clist)
        nodelist=[('Id','Label','Modularity')]
        for n in nodeset:
            nn=n.encode('utf-8')
            size=' '
            cat='cat'
            #if n in nodedict and nodedict[n]>40:
            #    size=nn
                #print size
            #    logging.info(size)
            size=nn
            if n in dstcat:
                cat=dstcat[n]
                cat=cat.encode('utf-8')
            nodelist.append((nn,size,cat))
        self.write_csv(node_filename,nodelist)
        #for a,b in sorted(nodedict.items(),key=lambda x:x[1],reverse=True)[:30]:
        #    print a,b
            
    
    def title_regrex_collect(self,title):
        rtitle=re.compile(title)
        for r in self.mp.link.find({"src_title":rtitle}):
            if 'src_is_act' in r and 'dst_is_act' in r:
                msg="%s %s %s %s" % (r['src_is_act'],r['src_title'],r['dst_title'],r['dst_is_act'])
                logging.info(msg)
    def groupby_cat(self):
        tdict={'cat':True}
        r=self.mp.groupby_cat('base',tdict)
        catset=set()
        for c in r:
            catset.add(c['cat'])
        return catset
def remove_csv(paths):
    for d in paths:
        gb=d+os.sep+'*.csv'
        for f in glob(gb):
            msg='remvoe %s'  % f
            logging.info(msg)
            os.remove(f)
def main():
    remove_csv(('csvdir','actcsv'))
    mp=mog_op.MongoOp('localhost')
    lc=LinkCheck(mp)
    catlist=lc.groupby_cat()
    #for c in catlist:
    #    lc.cat_collect(c)
    lc.act_collect()
    #lc.title_regrex_collect(u"日本国憲法[^の]")
    
if __name__=='__main__':main()
