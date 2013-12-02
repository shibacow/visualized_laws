#!/usr/bin/python
# -*- coding:utf-8 -*-
from mog_op import MongoOp
from pyquery import PyQuery as pq
from urlparse import urljoin
import re
import requests
from urllib import unquote
from datetime import datetime
import time

headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
         'Host':'law.e-gov.go.jp',
         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Language":"en-us,en;q=0.5",
         "Accept-Encoding":"gzip, deflate",
         "Cookie": "TS43e943=e5f00dce520074966860eba913b7188fa3f10512906644fa529ac63a",
         "Connection": "keep-alive"
         }

src='http://law.e-gov.go.jp/'

class GetRef(object):
    def __init__(self,mp):
        self.srcdict={}
        for m in mp.law_base.find():
            body=m['body']
            d=pq(body)
            self.parse_a(m,d)
        #print len(self.srcdict)
            
    def parse_a(self,m,d):
        for a in d('a'):
            ad=pq(a)
            href=ad.attr.href
            if href and re.search('^/cgi-bin/idxrefer.cgi',href):
                url=urljoin(src,href)
                self.srcdict.setdefault(url,0)
                self.srcdict[url]+=1
    def parse_params(self,a):
        a=a.split('?')[1]
        kdict={}
        for q in a.split('&'):
            k,v = q.split('=')
            kdict[k]=v
        for k in kdict:
            v=kdict[k]
            v=unquote(v)
            v=unicode(v,'cp932')
            print k,v
    def get_content(self,url,name):
        r=requests.get(url)
        content=unicode(r.content,'cp932')
        d=pq(content)
        title=d('html > body > b')
        title=title.text()
        return title
    def get_urlinfo(self,mp):
        size=len(self.srcdict)
        for i,(a,b) in enumerate(sorted(self.srcdict.items(),key=lambda x:x[1],reverse=True)):
            #self.parse_params(a)
            #print b,a
            r=requests.get(a)
            t=unicode(r.content,'cp932')
            c=pq(t)
            for f in c('frameset > frameset > frame'):
                f2=pq(f)
                ssk=f2.attr.src
                name=f2.attr.name
                if name=='inyotitle':
                    url=urljoin(src,ssk)
                    #mpf=mp.ref.find_one({'url':a})
                    #print url,mpf
                    if not mp.ref.find_one({'url':a}):
                        title=self.get_content(url,name)
                        if title:
                            print title
                            d={'url':a,'title':title,'created_at':datetime.now()}
                            mp.save('ref_title',d,'url')
                    else:
                        if i%10==0:
                            print 'i=%d alreday read' % i
                        pass
            if i%100==0:
                print "size=%d i=%d part=%d %%" % (size,i,(i*100)/size)
                time.sleep(10)

def main():
    mp=MongoOp('192.168.1.9')
    gf=GetRef(mp)
    gf.get_urlinfo(mp)
if __name__=='__main__':main()
