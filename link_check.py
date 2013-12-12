#!/usr/bin/python
# -*- coding:utf-8 -*-
import mog_op
from pyquery import PyQuery as pq
import re
from urlparse import urljoin
from bson.objectid import ObjectId
import csv

src='http://law.e-gov.go.jp/'
class RefCase(object):
    def __init__(self,source,ref):
        self.source=source
        self.ref=ref
        

class LinkCheck(object):
    def __init__(self,mp):
        self.mp=mp
        #self.matcher=re.compile('^([u（]+)')
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
        for i,l in enumerate(self.mp.law_base.find({"children":{"$size":0}})):
            body=l['body']
            body=pq(body)
            csize=self.pickup_link(l,body)
            print i,csize,l['title']
            l=None
    def check(self):
        for i,k in enumerate(self.mp.law_base.find({"children":{"$size":0}})):
            print i,len(k['children'])
    def cat_check(self,cat):
        for i,k in enumerate(self.mp.law_base.find({"cat":cat})):
            print i,k['cat'],k['title']
        
    def __lspliter(self,s):
        cc=s.split(u'（')
        
        #assert(len(cc)==2)
        if len(cc)>3:
            cc=cc[1:]
            #for i,c in enumerate(cc):
            #    print i,c
        if len(cc)>1:
            return cc[0]
        else:
            return []
    def write_csv(self,cname,clist):
        cout=csv.writer(open(cname,'ab'))
        cout.writerows(clist)
            
    def check_link(self):
        cnt=0
        srcdict={}
        for i,k in enumerate(self.mp.law_base.find()):
            #print i
            for c in k['children']:
                tt=self.mp.ref.find_one({"_id":c})
                dst=self.__lspliter(k['title'])
                source=self.__lspliter(tt['title'])
                if source and dst:
                    cnt+=1
                    #print cnt,i,kt,ttt
                    srcdict.setdefault(source,{})
                    srcdict[source].setdefault(dst,[])
                    srcdict[source][dst].append(RefCase(source,dst))
        srclist= sorted(srcdict.items(),key=lambda x:len(x[1]),reverse=True)
        srccsvs=[('Id','Label','Ref_size')]
        dstcsvs=[('source','target')]
        for i,(a,b) in enumerate(srclist):
            print '-'*60
            print len(b),a
            distdict=srcdict[a]
            for c,d in sorted(distdict.items(),key=lambda x:len(x[1]),reverse=True):
                #print '\t',c,len(d)
                dstcsvs.append((c.encode('utf-8'),a.encode('utf-8'),len(d)))
            srccsvs.append((a.encode('utf-8'),a.encode('utf-8'),len(b)))
            if i%1000==0:
                self.write_csv('node.csv',srccsvs)
                srccsvs=[]
                self.write_csv('edges.csv',dstcsvs)
                dstcsvs=[]
        self.write_csv('node.csv',srccsvs)
        srccsvs=[]
        self.write_csv('edges.csv',dstcsvs)
        dstcsvs=[]
    def remove_chapter(self,s):
        cc=s.split(u'「')[0]
        return cc
        
    def ref_link(self):
        
        for i,k in enumerate(self.mp.law_base.find()):
            for c in k['children']:
                tt=self.mp.ref.find_one({"_id":c})
                pt=tt['title']
                st=k['title']
                ptt=self.remove_chapter(pt)
                ptt=ptt.strip()
                #print "=%s=" % ptt
                kq=self.mp.law_base.find_one({'title':ptt})
                if not kq:
                    pass
                    #print st,"\n\t",ptt
            #if i%10==0:
               # print i

def main():
    mp=mog_op.MongoOp('localhost')
    lc=LinkCheck(mp)
    #lc.split_law_name()
    #lc.check()
    #lc.check_link()
    #lc.cat_check(u"刑事")
    lc.ref_link()

if __name__=='__main__':main()
