#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
sys.path.append('../lib')
sys.path.append('lib')
from law_info import ChangeWareki
import codecs
import unittest
from datetime import datetime
class TestWareki(unittest.TestCase):
    CLS_RESOURCE_LIST=[]
    @classmethod
    def setUpClass(cls):
        for l in codecs.open('resouce.txt',encoding='utf-8').readlines():
            l=l.strip()
            t=l.split(u',')
            cls.CLS_RESOURCE_LIST.append(t)
    def test_change(self):
        for l in self.CLS_RESOURCE_LIST:
            dkt={}
            dkt['title']=l[0]
            dkt['wareki']=l[1]
            dkt['date']=datetime.strptime(l[2],'%Y-%m-%d %H:%M:%S')
            dkt['drecree_number']=int(l[3])
            dkt['author']=l[4]
            tl=dkt['title']
            ch=ChangeWareki(tl)
            ch.conv_date(tl)
            ch.conv_go(tl)
            info=ch.get_info()
            self.assertEqual(info['created_date'],dkt['date'])

def main():
    unittest.main()

if __name__=='__main__':main()
