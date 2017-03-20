#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os

from mog_op import NewMongoOp
import logging
from datetime import datetime
from collections import Counter
from kanji2arabic import kansuji2arabic

log_fmt = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO,format=log_fmt)

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
        ss=re.findall(u"（(.*?)）",s)
        if ss:
            s2=ss[-1].split(u'日')[0]+u'日'
            self.nen=s2[:2]
            t=re.search(u"(.*)年(.*)月(.*)日",s2[2:])
            nen=self.__parse_kanji(t.group(1))
            month=self.__parse_kanji(t.group(2))
            day=self.__parse_kanji(t.group(3))
            #print self.title,self.nen
            year=jc[self.nen]+nen
            #print s2,year,nen,month,day
            self.wareki=s2
            self.date=datetime(year,month,day)
    def __parse_go(self,s):
        ss=re.findall(u"（(.*?)）",s)
        if ss:
            s2=u''.join(ss[-1].split(u'日')[1:])
            st=re.findall(u"^(.*?)第([壱一二弐三参四五六七八九十拾百千万萬億兆〇１２３４５６７８９０]+?)号$",s2)
            if st and len(st[0])==2:
                c=st[0][0]
                c1=st[0][1]
                c2=c1
                c2=re.sub(u"^百",u"一百",c2)
                c2=re.sub(u"^[十|拾]",u"一十",c2)
                c2=re.sub(u"百十",u"百一十",c2)
                c3=kansuji2arabic(c2)
                print "c1={} c3={} int_c3={}".format(c1.encode('utf-8'),c3.encode("utf-8"),int(c3))
            else:
                if not re.search(u"人事院規則|日本国憲法",self.title):
                    pass
                    #print len(st),self.title
                    #        print s
    def __init__(self,tl):
        self.wareki=None
        self.date=None
        self.title=tl
    def conv_date(self,s):
        s=s.strip()
        self.__parse_date(s)

    def conv_go(self,s):
        s=s.strip()
        self.__parse_go(s)

def check_created_date(mp):
    ycnt=Counter()
    for i,c in enumerate(mp.col.find()):
        tl=c['title']
        cw=ChangeWareki(tl)
        cw.conv_date(tl)
        date=cw.date
        year=date.year
        month=date.month
        day=date.day
        ycnt[year]+=1
        cw.conv_go(tl)
        #msg="i={} date={}-{}-{} title={}".format(i,year,month,day,tl.encode("utf-8"))
        #logging.info(msg)
    #for a,b in sorted(ycnt.most_common()):
    #    print a,b
def duplicate_check(mp):
    cnt=Counter()
    for c in mp.col.find():
        tl=c['title']
        cnt[tl]+=1
    for k,c in cnt.most_common(100):
        if c>1:
            print c,k
def main():
    mp=NewMongoOp('localhost')
    check_created_date(mp)
    #duplicate_check(mp)
if __name__=='__main__':main()
