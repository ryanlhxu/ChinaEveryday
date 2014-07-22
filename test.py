#coding:utf-8
import urllib
import time
"""
<tr><td valign="top" bgcolor="#ffffff" width="7%">
<a href="http://www.nber.org/papers/w20298"> w20298 </a></td>
<td valign="top" bgcolor="#ffffff" width="23%"> <nobr>Lorenz Kueng<br>  Evgeny Yakovlev</nobr> <br></td>
<td valign="top" bgcolor="#ffffff" width="70%">How Persistent Are Consumption Habits? Micro-Evidence from Russia's Alcohol Market<p></td></tr>
"""
####################################


class article:
    def __init__(self,url):
        self.url=url 
    def abstract(self):
        con = urllib.urlopen(self.url).read()
        initial = con.find(r'margin-left') 
        abs_init = con.find(r'justify">',initial)
        abs_end = con.find(r'</p>',abs_init)
        abs_con = con[abs_init+10:abs_end]
        return abs_con


"""       
<p style="margin-left: 40px; margin-right: 40px; text-align: justify">
Does information asymmetry affect the cross-section of expected stock returns? Using institutional ownership data from the Shanghai Stock Exchange, we show that institutions have a strong information advantage over individual investors. We then show that the aggressiveness of institutional trading in a stock—measured by the average absolute weekly change in institutional ownership during the past year—is an ex ante predictor of future information asymmetry in this stock. Sorting stocks on this information asymmetry predictor, we find that the top quintile outperforms the bottom quintile next month by 10.8% annualized, suggesting that information asymmetry raises the cost of capital.
</p>
"""

con = urllib.urlopen('http://www.nber.org/workinggroups/papers/CE.html').read()
initial = con.find(r'<tr><td valign="top" bgcolor="#ffffff" width="7%">')
maxit=200
item=0
url=[]
title=[]
while item < maxit:
    href_init = con.find(r'href="',initial)
    if href_init == -1:
        break
    else:
        href_end = con.find(r'"> w',href_init)
        title_init = con.find(r'"70%',href_end)
        title_end = con.find(r'<p></td></tr>',title_init)
        url.append(con[href_init+6:href_end])
        title.append(con[title_init+6:title_end])
        initial= con.find(r'<tr><td valign="top" bgcolor="#ffffff" width="7%">',title_end)
        item +=1

i=0
article = article(url[i])
abs_con = article.abstract()

file1 = open('ChineseEconomy/china.txt','a')
file1.write(title[i])
file1.write('\n'+ abs_con)
file1.close()



