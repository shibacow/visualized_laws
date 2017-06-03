#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def kansuji2arabic(text):
    """漢数字からアラビア数字への変換"""
    KANNUM_PATTERN = re.compile(u'(?P<kansuji>[壱一二弐三参四五六七八九十拾百千万萬億兆〇１２３４５６７８９０，,\d]+)')
    index = 0
    while index < len(text):
        matched = KANNUM_PATTERN.search(text[index:])
        if matched:
            kansuji = matched.group('kansuji')
            startindex = matched.start('kansuji') + index
            endindex = matched.end('kansuji') + index
            result = 0
            digit = 1
            numgroup = 1
            kanindex = len(kansuji)
            while kanindex > 0:
                c = kansuji[(kanindex - 1):kanindex]
                kanindex -= 1
                if c == u'〇０0':
                    digit *= 10
                elif c in u'十拾':
                    digit = 10
                elif c == u'百':
                    digit = 100
                elif c == u'千':
                    digit = 1000
                elif c in u'万萬':
                    numgroup = 10000
                    digit = 1
                elif c in u'億':
                    numgroup = 10000*10000
                    digit = 1
                elif c in u'兆':
                    numgroup = 10000*10000*10000
                    digit = 1
                elif c in u'，,':
                    pass
                else:
                  if c in u'壱一１1':
                      result += digit * numgroup
                  elif c in u'二弐２2':
                      result += 2 * digit * numgroup
                  elif c in u'三参３3':
                      result += 3 * digit * numgroup
                  elif c in u'四４4':
                      result += 4 * digit * numgroup
                  elif c in u'五５5':
                      result += 5 * digit * numgroup
                  elif c in u'六６6':
                      result += 6 * digit * numgroup
                  elif c in u'七７7':
                      result += 7 * digit * numgroup
                  elif c in u'八８8':
                      result += 8 * digit * numgroup
                  elif c in u'九９9':
                      result += 9 * digit * numgroup
                  digit *= 10
            text = u'%s%d%s' % (text[:startindex], result, text[endindex:])
            index = startindex + len('%d' % (result,))
        else:
              break
    return text

def main():
    examples = [u'平成２２年度一般会計予算は９２兆２２９２億円',
                u'平成22年度一般会計予算は９２兆２,２９２億円',
                u'平成22年度一般会計予算は９２兆２，２９２億円']
    for text in examples:
        print text, '->',kansuji2arabic(text)

if __name__ == '__main__':
    main()
