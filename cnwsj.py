# coding:utf-8
import re
import urllib
from HTMLParser import HTMLParser
import datetime
import time



class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url=[]
        self.parse_data_flag = False
        self.flag = False
        self.items = []
    
    def handle_starttag(self,tag,attrs):
        if tag=='a' and attrs:
            for key ,value in attrs:
                p_url = re.compile(r'20\d{6}/bch\d+.asp')   
                if key=='href' and p_url.match(value):
                   self.url = value
        if tag == "span" and self.parse_date == True :
            self.date_start = True
                         
    def handle_data(self,data):
        #处理数据
        if self.flag == True :
            self.text = data
        if self.date_start == True :
            self.items.append((self.text,self.url))
                   
    #def handle_data(self,data):
      #  print unicode(data,'gbk')
    def get_items(self):
        return self.items

parser = MyHTMLParser()

con = urllib.urlopen('http://cn.wsj.com/gb/bch.asp').read()

p_china_new  = re.compile(r'<div id="t2lnews2">[\s\S]+top2right"')
m_china_new = p_china_new.search(con)
china_new = m_china_new.group()

item = []
p_item = re.compile(r'<a href.+</div>')
m_item = p_item.finditer(china_new)
for i in m_item:
    item.append(i.group())

parser.feed(china_new)
items = parser.get_items()
#for i in url:
print items


