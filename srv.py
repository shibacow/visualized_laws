#!/usr/bin/python
# -*- coding:utf-8 -*-
import web
urls=('/.*','Index')
render=web.template.render('template')
class Index(object):
    def GET(self,*args,**keys):
        d={}
        return render.index(d)

app=web.application(urls,globals())
def main():
    app.run()

if __name__=='__main__':main()
