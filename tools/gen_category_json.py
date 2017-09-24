#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging
import json
from glob import glob
import re
logging.basicConfig(level=logging.DEBUG,\
                        format="%(asctime)s %(levelname)s %(message)s")
src="../../visualized_laws_web/app/data/category.json"
dst="../../visualized_laws_web/app/data/category2.json"
addurldir="../addurl/*.gexf"

def main():
    dkt={}
    for f in glob(addurldir):
        cn=re.findall('\.\./addurl/(.*)\.gexf',f)[0]
        cn=unicode(cn,'utf-8')
        cn=cn.encode('utf-8')
        dkt[cn]=cn
        print(cn)
    r=json.dump(dkt,open(dst,'wb'),ensure_ascii=False)
    print(r)
if __name__=='__main__':main()
