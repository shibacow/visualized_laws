#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import requests
import mechanize
import json
import dotenv
from pyquery import PyQuery as pq
import time
import urlparse
import pymongo
import os
from dotenv import load_dotenv, find_dotenv
import logging
log_fmt = '%(asctime)s- %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO,format=log_fmt)

load_dotenv(find_dotenv())
MONGO_DB=os.environ.get("MONGO_DB")

base_url="http://law.e-gov.go.jp/cgi-bin/idxsearch.cgi"

headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Encoding":"gzip, deflate",
         "Accept-Language":"ja,en-US;q=0.7,en;q=0.3",
         "Connection":"keep-alive",
         "Host":"law.e-gov.go.jp",
         "Referer":"http://law.e-gov.go.jp/cgi-bin/idxsearch.cgi",
         "Upgrade-Insecure-Requests":"1",
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }

def get_data(category_id):
    params={
        category_id:u"　",
        "H_CTG_GUN":1,
        "H_NAME":0,
        "H_NAME_YOMI":u"　",
        "H_NO_GENGO":"H",
        "H_NO_NO":0,
        "H_NO_TYPE":2,
        "H_NO_YEAR":0,
        "H_RYAKU":1,
        "H_YOMI_GUN":1
    }
    r=requests.post(base_url,data=params,headers=headers)
    if r.status_code == requests.codes.ok:
        r.encoding="SHIFT_JIS"
        return r.text
    else:
        return None
def pickup(r):
    cat=re.search(u"事項別索引指定　「(.*)」（全法令）",r)
    c=cnt=None
    if cat:
        c=cat.group(1)
        c=re.sub(u"　",u'',c)
    count=re.search(u"該当件数(.*) 件",r)
    if count:
        cnt=count.group(1)
        cnt=re.sub(u"　",u'',cnt)
        cnt=int(cnt)
    return c,cnt

class Law(object):
    def __init__(self,cat,cat_num,link,title):
        self.title=title
        self.link=urlparse.urljoin(base_url,link)
        self.cat=cat
        self.cat_num=cat_num
    def __str__(self):
        return "cat={} cat_num={} link={} title={}".format(self.cat.encode('utf-8'),self.cat_num,self.link,self.title.encode('utf-8'))
    def get_data(self,url,conv_pq=True):
        r=requests.get(url,headers=headers)
        if r.status_code == requests.codes.ok:
            r.encoding="SHIFT_JIS"
            if conv_pq:
                return pq(r.text)
            else:
                return r.text
        else:
            return None
    def get_body(self):
        d=self.get_data(self.link)
        if d:
            head=d('frame[name="title"]')
            headlink=urlparse.urljoin(base_url,head.attr('src'))
            headd=self.get_data(headlink)
            self.headtitle=headd.text()
            history=headd('a[href^="http://hourei.ndl.go.jp/"]')
            self.history=history.attr("href")
            body=d('frame[name="data"]')
            self.bodylink=urlparse.urljoin(base_url,body.attr("src"))
            self.body=self.get_data(self.bodylink,conv_pq=False)
        else:
            logging.warning("nothing link={}".format(link))
    def get_dict(self):
        dkt=dict(title=self.title,link=self.link,cat=self.cat,cat_size=self.cat_num,
                    history_link=self.history,headtitle=self.headtitle,body_link=self.bodylink,
                    body=self.body)
        return dkt

class MongoOp(object):
    def __init__(self,host):
        self.con=pymongo.MongoClient(host,27017)
        self.db=self.con[MONGO_DB]
        self.col=self.db.laws
    def insert(self,dkt):
        title=dkt['title']
        if not self.col.find_one({"title":title}):
            self.col.insert_one(dkt)
    def has_one(self,title):
        return self.col.find_one({"title":title})

def parse(r,i,laws):
    cat,cat_cnt=pickup(r)
    d=pq(r)
    logging.info("i={} cat={}".format(i,cat.encode('utf-8')))
    for k in d('a'):
        k=pq(k)
        link=k.attr('href')
        title=k.text()
        laws.append(Law(cat,cat_cnt,link,title))

def crawl_data(mp):
    start=1
    end=50
    laws=[]
    for i in range(1,end+1):
        time.sleep(1)
        h_ctg="H_CTG_{}".format(i)
        r=get_data(h_ctg)
        if r:
            parse(r,i,laws)
    size=len(laws)
    for i,l in enumerate(laws):
        logging.info("i={} size={} title={}".format(i,size,l.title.encode('utf-8')))
        if mp.has_one(l.title):
            logging.info("title={} alredy have".format(l.title.encode("utf-8")))
            continue
        time.sleep(1)
        l.get_body()
        dkt=l.get_dict()
        mp.insert(dkt)
def validate_data(mp):
    for dkt in mp.col.find().limit(1):
        bd=dkt['body']
        logging.info(bd)
def main():
    mp=MongoOp('localhost')
    #validate_data(mp)
    crawl_data(mp)
if __name__=='__main__':main()
