#!/usr/bin/env python
# -*- coding:utf-8 -*-
from mog_op import MongoOp
from pyquery import PyQuery as pq
import re
from datetime import datetime

class ChangeWareki(object):
    def __parse_kanji(self,p):
        yn={u"一":1,
            u"元":1,
            u"二":2,
            u"三":3,
            u"四":4,
            u'五':5,
            u'六':6,
            u'七':7,
            u'八':8,
            u'九':9,
            u'十':10
        }
        p=p.split(u'十')
        p.reverse()
        nm=0
        for i,j in enumerate(p):
            ppk=yn.get(j,i)
            nm+=ppk*(10**i)
        return nm
    def __parse_date(self,s):
        jc={u"平成":1988,
            u"昭和":1925,
            u"大正":1911,
            u"明治":1867}
        ss=re.findall(u"（(.*)）",s)
        if ss:
            s2=ss[0].split(u'日')[0]+u'日'
            self.nen=s2[:2]
            t=re.search(u"(.*)年(.*)月(.*)日",s2[2:])
            nen=self.__parse_kanji(t.group(1))
            month=self.__parse_kanji(t.group(2))
            day=self.__parse_kanji(t.group(3))
            year=jc[self.nen]+nen
            #print s2,year,nen,month,day
            self.wareki=s2
            self.date=datetime(year,month,day)
    def __parse_go(self,s,title):
        ss=re.findall(u"（(.*)）",s)
        if ss:
            s2=u''.join(ss[0].split(u'日')[1:])
            st=re.findall(u"(.*?)第(.*?)号",s2)
            if st and len(st[0])==2:
                c=st[0][0]
                c2=st[0][1]
                #print c2
            else:
                if not re.search(u"人事院規則",s2):
                    print title,s
    def __init__(self):
        self.wareki=None
        self.date=None
    def conv_date(self,s):
        s=s.strip()
        self.__parse_date(s)

    def conv_go(self,s,title):
        s=s.strip()
        self.__parse_go(s,title)

def parse(l):
    title=l['title']
    d=pq(l['body'])
    b=d('b:first')
    html=b.html()
    s=html.split("<br/>")
    ch=ChangeWareki()
    ch.conv_date(s[-1])
    ch.conv_go(s[-1],title)

def main():
    mp = MongoOp('localhost')
    for l in mp.law_base.find():
        parse(l)
if __name__=='__main__':main()
