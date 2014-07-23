# coding=UTF-8
import re
import urllib
import time

max_page = 3
page = 0
date = []
title = []
abstract = []
url = []
date_local = time.strftime('%Y年%m月%d日',time.localtime(time.time()))
exit = 0

while page < max_page and exit==0:
    
    # acquire the date
    if page > 0:
        page_url = r'http://wallstreetcn.com/china?' + (page>0)*'page=%d'  %page    
    else:
        page_url = r'http://wallstreetcn.com/china'
    
    con = urllib.urlopen(page_url).read()
    
    p_date  = re.compile(r'<span class="meta-item">\s+\d+年\d+月\d+日')
    m_date = p_date.finditer(con)
    for i in m_date:
        date.append(''.join(i.group().split())[23:])
    
    for i in date:
        if i != date_local:
            exit=1
            break
        else:
            pass
    print exit, date[1]
    
    #acquire the url and title
    p_url = re.compile(r'<h2><a href="/node/\d+" target="_blank">.+')
    m_url = p_url.finditer(con)
    for i in m_url:
        url.append(r'http://wallstreetcn.com'+i.group()[13:25])
        title.append(i.group()[43:-9])

    #acquire the abstract
    p_abstract= re.compile(r'media-content">\s+<p>.+')
    m_abstract = p_abstract.finditer(con)
    for i in m_abstract:
        abstract.append(''.join(i.group().split())[18:-4])
    page+=1


for i, date_i in enumerate(date): 
    if date_i ==date_local:
        print '%s: %s\n%s: %s\n%s: %s\n\n'  %('标题', title[i], '摘要', abstract[i],'地址',url[i])

