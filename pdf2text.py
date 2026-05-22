#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import re
import logging
logging.basicConfig(level=logging.INFO)
import os

def gettext(pdfname):
    # PDFファイル名が未指定の場合は、空文字列を返して終了
    if (pdfname == ''):
        return ''
    else:
        # 処理するPDFファイルを開く/開けなければ
        try:
            fp = open(pdfname, 'rb')
        except Exception as err:
            logging.error('pdf={} err={}'.format(pdfname,err))
            return ''
    
    # リソースマネージャインスタンス
    rsrcmgr = PDFResourceManager()
    # 出力先インスタンス
    outfp = StringIO()
    # パラメータインスタンス
    laparams = LAParams()
    # 縦書き文字を横並びで出力する
    laparams.detect_vertical = True
    # デバイスの初期化
    device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams)
    # テキスト抽出インタプリタインスタンス
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # 対象ページを読み、テキスト抽出する。（maxpages：0は全ページ）
    for page in PDFPage.get_pages(fp, pagenos=None, maxpages=0, password=None,caching=True, check_extractable=True):
        interpreter.process_page(page)
        #取得したテキストをすべて読みだす
        ret = outfp.getvalue()
        # 後始末をしておく
    fp.close()
    device.close()
    outfp.close()
    # 空白と改行をとりさり一塊のテキストとして返す
    return re.sub(r"\s|　",'',ret)

def main():
    pdfs = []
    pdfsrc='/home/shibacow/prog/fetch_law_data/pdfs/'
    for root,dirs,files in os.walk(pdfsrc):
        for f in files:
            if re.search('\.pdf$',f):
                pp=root+os.sep+f
                #print(pp)
                pdfs.append(pp)
    sz=[]
    for pp in pdfs[:100]:
        result = gettext(pp)
        #print(len(result))
        lensz=len(result)
        sz.append((lensz,pp))
    for s,p in sz:
        print('size={} p={}'.format(s,p))
if __name__=='__main__':main()
