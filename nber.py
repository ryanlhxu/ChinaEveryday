# coding:utf-8
import re
import urllib
from HTMLParser import HTMLParser
import datetime
import MySQLdb

conn = MySQLdb.connect(user='root',passwd='',host='localhost')
cur = conn.cursor()
conn.select_db('xuliheng')


class author_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.flag = False
        self.author = ''
        self.author_url = ''
        self.item = {}
    def handle_starttag(self,tag,attrs):
        if tag == 'a' and attrs:
            for key, value in attrs:
                if key == 'href':
                    self.flag = True
                    self.author_url+=value[8:]+'|'

    def handle_data(self,data):
        if self.flag == True:
            self.author+=data+'|'
    def handle_endtag(self,tag):
        #处理结束标签
        if tag == 'a':
            self.flag=False  
    def get_item(self):
        self.item['author'] = self.author
        self.item['author_url'] = self.author_url
        return self.item

cur.execute("select * from nber order by article_id desc limit 0,1")
start_article_id =  cur.fetchone()[0]+1
maxits = 10
items = []
its = 0
flag = True

while its<maxits and  flag == True:
    print its
    start_article_url = 'http://www.nber.org/papers/w'+str(start_article_id)
    con = urllib.urlopen(start_article_url).read()
    read_flag = con.find(r'Paper Not Found')
    
    if read_flag != -1:
        next_article_url = 'http://www.nber.org/papers/w'+str(start_article_id+1)
        next_con = urllib.urlopen(next_article_url).read()
        next_read_flag = next_con.find(r'Paper Not Found')
        if next_read_flag !=-1:
            flag = False
            break
        else:
            start_article_id +=1
            its+=1
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
        item['article_id'] = start_article_id
        items.append(item)
        its+=1
        start_article_id+=1

f_add = "insert into nber(article_id,author,author_url,title,abstract) value(%s,%s,%s,%s,%s)"
#items = [{'id':1,'title':'hello'},{'id':2,'title':'world'}]
for item in items:
    c_add = (item['article_id'],item['author'],item['author_url'],item['title'],item['abstract'])
    cur.execute(f_add, c_add)

cur.close()
conn.commit()
conn.close()


