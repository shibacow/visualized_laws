#!/usr/bin/env python
# -*- coding:utf-8 -*-

cat=u"""憲　法 
刑　事 
財務通則 
水産業 
観　光
国　会 
警　察 
国有財産 
鉱　業 
郵　務
行政組織 
消　防 
国　税 
工　業 
電気通信
国家公務員 
国土開発 
事　業 
商　業 
労　働
行政手続 
土　地 
国　債 
金融・保険 
環境保全
統　計 
都市計画 
教　育 
外国為替・貿易 
厚　生
地方自治 
道　路 
文　化 
陸　運 
社会福祉
地方財政 
河　川 
産業通則 
海　運 
社会保険
司　法 
災害対策 
農　業 
航　空 
防　衛
民　事 
建築・住宅 
林　業 
貨物運送 
外　事"""

import re
import yaml

def makematrix():
    catlist=[]
    ct=[]
    for i,l in enumerate(cat.split('\n')):
        l=l.strip()
        l=re.sub(u'[ 　]','',l)
        ct.append(l)
        print(ct)
        if i>0 and (i+1)%5==0:
            catlist.append(ct)
            ct=[]
        print u"={}=".format(l)
    if ct:
        catlist.append(ct)
    return catlist

def inverth(matrix):
    cat2=[]
    for i in range(5):
        for j in range(10):
            cat2.append(matrix[j][i])
    return cat2
def genhsbhash(cat2list):
    configdict={
        "NODE_BORDER":True,
        "COLORS":{}
    }
    for i ,a in enumerate(cat2list):
        h=(i/50.0)
        s=1.0
        b=0.8
        dkt=dict(h=h,s=s,b=b)
        configdict['COLORS'][a]=dkt
    with open("../config/config.yaml",'w') as outfile:
        yaml.dump(configdict,outfile,allow_unicode=True)
def main():
    matrix=makematrix()
    cat2list=inverth(matrix)
    genhsbhash(cat2list)
if __name__=='__main__':main()

