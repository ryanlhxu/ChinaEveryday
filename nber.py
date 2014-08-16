# coding:utf-8
import re
import urllib
from HTMLParser import HTMLParser
import datetime
import time

class author_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.author = []
        self.author_url = []
        self.item = {}
    def handle_starttag(self,tag,attrs):
        if tag == 'a' and attrs:
            for key, value in attrs:
                if key == 'href':
                    self.flag = True
                    self.author_url.append('http://www.nber.org'+value)

    def handle_data(self,data):
        if self.flag == True:
            self.author.append(data)
    def handle_endtag(self,tag):
        #处理结束标签
        if tag == 'a':
            self.flag=False  
    def get_item(self):
        self.item['author'] = self.author
        self.item['author_url'] = self.author_url
        return self.item

start_article_id =  20500
maxits = 5
items = []
its = 0
flag = True

while its<maxits and  flag == True:
    print its
    start_article_url = 'http://www.nber.org/papers/w'+str(start_article_id)
    con = urllib.urlopen(start_article_url).read()
    read_flag = con.find(r'Paper Not Found')
    if read_flag != -1:
        flag = False
        break
    else:
        initial = con.find(r'<div id="mainNewsDiv">')
        title_initial = con.find(r"title'>",initial)
        title_end = con.find(r'</h1>',title_initial)
        title = con[title_initial+7:title_end]
        author_initial = con.find(r"<h2 class='bibtop",title_end) 
        author_end = con.find(r'</h2>',author_initial)
        author_con = con[author_initial:author_end]
        parser = author_parser()
        parser.feed(author_con)
        item = parser.get_item()
        abstract_initial = con.find(r'justify">',author_end)
        abstract_end = con.find(r'</p>',abstract_initial)
        abstract = con[abstract_initial+10:abstract_end-1]
        item['abstract']  = abstract
        item['title'] = title
        items.append(item)
        its+=1
        start_article_id+=1
