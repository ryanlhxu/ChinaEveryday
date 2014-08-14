# coding:utf-8
import re
import urllib
from HTMLParser import HTMLParser
import datetime
import time

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.url_temp = ''
        self.url=[]
        self.title = []
        self.abstract = []
        self.items = []
        self.parse_data_flag = False
        self.flag = False
        self.data_start = False
        self.title_flag = False
        self.div_flag = False
        self.data_start_abstract = False
    def handle_starttag(self,tag,attrs):
        if tag == 'div' and attrs:
            for key,value in attrs:
                if key == 'style' and value == 'font-size:14px;line-height:140%;padding-bottom:10px;text-decoration:none;color:#555;font-weight:normal;overflow:hidden;':
                    self.div_flag = True
        if tag=='a' and attrs:
            for key ,value in attrs:
                p_url = re.compile(r'20\d{6}/b\S{2}\d+.asp')   
                if key=='href' and p_url.match(value):
                   self.url_temp= value
                   self.flag = True
        if tag == "span" and attrs:
            for key, value in attrs:
                if key == 'style' and value == 'font-weight:bolder;':
                    self.title_flag=True
            self.abstract_flag = False
            self.data_start_abstract = False
        if self.title_flag == True and self.flag == True:
            self.data_start = True     
        if self.div_flag == True and self.abstract_flag == True:
            self.data_start_abstract = True

    def handle_data(self,data):
        #处理数据
        if self.data_start:
            self.url.append(self.url_temp)
            self.title.append(data)
        if self.data_start_abstract: 
            if data != r'[\n\r ]':
                self.abstract.append(''.join(data.split())) 

    def handle_endtag(self,tag):
        #处理结束标签
        if tag == 'a':
            self.flag=False
            self.abstract_flag = True

        if tag == 'span':
            self.title_flag = False
            self.data_start = False
        if tag == 'div':
            self.div_flag = False
            self.data_start_abstract = False
    
    def get_items(self):
        for i in range(len(self.url)):
            my_url = ''.join(self.url[i].split('/'))
            self.items.append({'title':self.title[i].decode('gbk'),"my_url":'/cnwsj/'+my_url,'abstract':unicode(self.abstract[2*i+1],'gbk')})    
        return self.items


def cnwsj():
    parser = MyHTMLParser()
    con = urllib.urlopen('http://cn.wsj.com/gb/bch.asp').read()
    p_china_new  = re.compile(r'<div id="t2lnews2">[\s\S]+top2right"')
    m_china_new = p_china_new.search(con)
    china_new = m_china_new.group()
    parser.feed(china_new)
    items = parser.get_items()
    return items
