#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os

from mog_op import NewMongoOp
import logging
from datetime import datetime
from collections import Counter
from kanji2arabic import kansuji2arabic
import codecs

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
        else:
            #wrong path
            assert(False)
    def __parse_nums(self,nums):
        digit=0
        nums2=nums[::-1]
        yn={u"一":1,
            u"―":1,
            u"元":1,
            u"二":2,
            u"三":3,
            u"四":4,
            u'五':5,
            u'六':6,
            u'七':7,
            u'八':8,
            u'九':9,
            u'十':10,
            u"○":0,
            u"〇":0,
        }

        for i,c in enumerate(nums2):
            k=yn[c]
            digit+=k*10**i
        return digit
    def __parse_go(self,s):
        ss=re.findall(u"（(.*?)）",s)
        if ss:
            #[FIXME]日が、公布日だけでなく、日本にもマッチしてしまう
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
                self.authorities=c
                self.law_number=int(c3)
            else:
                if re.search(u"人事院規則",self.title):
                    nums=re.findall(u"^人事院規則([壱一二弐三参四五六七八九十〇―一]*)",self.title)
                    if nums:
                        nums=nums[0]
                        self.authorities=u"人事院規則"
                        self.law_number=self.__parse_nums(nums)
                elif re.search(u"日本国憲法",self.title):
                    self.authorities=u"日本国憲法"
                    self.law_number=0
                else:
                    self.authorities=s2
                    self.law_number=0
        assert(self.authorities!=None)
        assert(self.law_number!=None)
    def __init__(self,tl):
        self.title=tl
        self.date=None
        self.wareki=None
        self.law_number=None
        self.authorities=None
    def conv_date(self,s):
        s=s.strip()
        self.__parse_date(s)
    def conv_go(self,s):
        s=s.strip()
        self.__parse_go(s)
    def get_info(self):
        return dict(wareki=self.wareki,created_date=self.date,\
                    decree_number=self.law_number,authorities=self.authorities)

def check_created_date_and_auth(mp):
    out=codecs.open("resouce.txt",'wb',encoding='utf-8')
    for i,c in enumerate(mp.col.find()):
        tl=c['title']
        cw=ChangeWareki(tl)
        cw.conv_date(tl)
        cw.conv_go(tl)
        info=cw.get_info()
        c['wareki']=info['wareki']
        c['created_date']=info['created_date']
        c['decree_number']=info['decree_number']
        c['authorities']=info['authorities']
        #mp.col.update({"title":tl},c)
        #logging.info(info)
        msg=u"{},{},{},{},{}\n".format(tl,info['wareki'],info['created_date'],info['decree_number'],info['authorities'])
        print(msg)
        out.write(msg)
    out.close()
def duplicate_check(mp):
    cnt=Counter()
    for c in mp.col.find():
        tl=c['title']
        cnt[tl]+=1
    for k,c in cnt.most_common(100):
        if c>1:
            print c,k
def check_authorities(mp):
    cnt=Counter()
    sz=Counter()
    for c in mp.col.find():
        auth=c['authorities']
        #if not re.search(u"法律|政令|省令|勅令",auth):
        if re.search(u"本",auth):
            cnt[auth]+=1
        sz[auth]=len(auth)
    for a,b in cnt.most_common():
        print a,b
    #for a,b in sz.most_common(20):
    #    print a,b

def main():
    mp=NewMongoOp('localhost')
    check_created_date_and_auth(mp)
    #duplicate_check(mp)
    #check_authorities(mp)
if __name__=='__main__':main()
