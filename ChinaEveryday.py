# coding:utf-8
import re
import urllib
import datetime
from wsjcn import wsjcn_whichday
from cnwsj import cnwsj 
from flask import Flask,render_template,url_for
app = Flask(__name__)

@app.route('/')
def home():
    webs = [{'name':u'华尔街日报', 'my_url':'/wallstreetcn'},
    {'name':u'FT中文网','my_url':'/ft'}]
    return render_template('home.html')

@app.route('/wallstreetcn')
def wallstreetcn():
    date_local_uf = datetime.date.today()
    date_local = date_local_uf.strftime('%Y年%m月%d日')
    #date_local = '2014年08月13日'
    header = "华尔街见闻--%s"%date_local
    header = unicode(header,'utf-8')
    items = wsjcn_whichday(date_local)
    return render_template('index.html',header=header, items = items)

@app.route('/wallstreetcn/yesterday')
def wallstreetcn_yesterday():
    date_local_uf = datetime.date.today()
    date_yes_uf = date_local_uf + datetime.timedelta(days = -1)
    date_yes = date_yes_uf.strftime("%Y年%m月%d日") 
    header = "华尔街见闻--%s"%date_yes
    header = unicode(header,'utf-8')
    items = wsjcn_whichday(date_yes)
    return render_template('index.html',header=header, items = items)

@app.route('/wallstreetcn/<article_id>')
def article(article_id):
    url = 'http://wallstreetcn.com/node/'+ article_id
    con = urllib.urlopen(url).read()
    title_initial = con.find(r'page_sign">')
    title_end = con.find(r'</h1>',title_initial)
    title =  con[title_initial+16:title_end].decode('utf-8')
    main_initial = con.find(r'typo">',title_end)
    main_end = con.find(r'<!--',main_initial)
    main =  con[main_initial+11:main_end-2].decode('utf-8')
    main = main.replace('\n',' ')
    notice = u'文章来源于华尔街见闻，华尔街见闻微信号为wallstreetcn'
    #main =  """<p><img alt="" src="http://img.wallstreetcn.com/ckuploadimg/images/80032557(1).jpg" style="height:334px; width:500px" /></p> <p>“美国政府对俄罗斯施展更多制裁措施是一个严重的错误，那只会令已经紧绷的局势升级，并最终伤害美国经济。尽管短期效果不明显，但长期来看，制裁将反作用于美元，令其世界储备货币的角色消亡。”</p> <p>前美国参议员Ron Paul通过他主办的教育机构The Ron Paul Institute发表了上述观点。</p>         <p>Ron Paul是美国资深政治家，他曾在2008年美国总统竞选中失败。他的观点在美国政界显得尤为突出。比如，他主张“关闭美联储(End the fed)”，这个口号在今年的“占领华尔街”运动中与“We are the 99%”比肩齐名。他还支持大麻合法化。</p> <p>Ron Paul表示，</p> <blockquote><p>美国联合欧盟对俄施展愈加严厉的制裁措施恐伤及欧洲银行业，同时，美国还以违反自己的制裁令为由对部分欧洲银行开出巨额罚单，这将引发这些金融机构及其客户更加厌恶美国。</p> </blockquote> <p>华尔街见闻网站此前提及，法国就因该国第一大银行法国巴黎银行被罚近90亿美元巨款而心生不满，法国财长当时曾威胁称，中欧贸易就可以停止使用美元，转而使用欧元和人民币。欧洲第二大石油生产商道达尔首席执行官Christophe de Margerie也认为，没有理由以美元来支付石油款项。</p> <p>据IMF数据，截止去年底，美元在全球外储中占比为33%。这一比重自2000年以来就持续下降，当时比例为55%。</p> <p>不仅如此，由于美国不断加强打击美国公民海外避税逃税和洗钱的犯罪行为，还通过外交手段施压部分国家政府，迫使欧洲银行业不得不与美国开展合作。尤其是传统的“避税天堂”瑞士，多家银行被迫向美国国税局提交其美国公民的账户信息，令该国多年以来严守客户秘密的名节不保。为此，很多欧洲银行切断了与部分美国客户的业务往来。而一些持有巨额财富的美国公民也因此无法与部分国外银行建立良好的合作关系。</p> <p>Ron Paul认为，</p> <blockquote><p>可以预见，随着美国政府对欧洲银行业施加的压力越来越重，未来将有更多欧洲银行减少与美国和美元的联系，最终使得美国及美国公民被孤立。因此，从这个角度说，试图孤立俄罗斯实际上恰恰令美国自身画地为牢。</p> </blockquote> <p>对俄制裁的其他影响还包括将把俄罗斯推向其“金砖兄弟国家”的怀抱。Ron Paul表示，</p> <blockquote><p>金砖五国人口占全球比重为40%，其经济产出已经相当于美国和欧盟。这些国家还掌握着大量的自然资源。尤其是油气资源丰富的俄罗斯，该国自然资源为很多欧洲国家所高度依赖。</p> </blockquote> <p>华尔街见闻网站曾提及，俄罗斯的公司正在将合同转向用欧元、人民币和港元等其它货币结算，大型俄罗斯企业正将一部分现金转移到亚洲的银行。上周五，俄罗斯央行称，已和中国央行就本币互换协议达成一致。他还称，</p> <blockquote><p>如果这一趋势持续扩散，则将继续削弱美元在国际贸易中的地位。</p> </blockquote> <blockquote><p>更重要的可能是：中国、俄罗斯和南非合计供应着全球近40%的黄金。一旦这些国家决定开创并发行一种由黄金支撑的新货币，那么这将对美元构成新的挑战。</p> </blockquote> <blockquote><p>美国政府一直依赖与其他国家合作来维持美元的霸权地位。但国际社会的耐心正在减少，特别是近几十年来，胡萝卜+大棒的软硬兼施法已转变成只有大棒、没有胡萝卜。如果奥巴马总统和他的继任者出于自己不喜欢的原因而继续对其他国家施展严厉的制裁，那只会导致更多的国家回避美元，并加速美元滑向世界货币体系的边缘。</p> </blockquote> """
    #main = main.replace('\n',' ')
    #main = main.decode('utf-8')
    return render_template('post.html',title=title,notice=notice,main=main)

@app.route('/cnwsj')
def cnwallstreet():
    header = "华尔街日报"
    header = unicode(header,'utf-8')
    items = cnwsj()
    return render_template('index.html',header=header, items = items)

@app.route('/cnwsj/<article_id>')
def article_cnwsj(article_id) : 
    article_id= article_id[:8]+'/'+article_id[8:]
    url = 'http://cn.wsj.com/gb/'+ article_id
    con = urllib.urlopen(url).read()
    con = con.decode('gb2312')
    title_initial = con.find(r'id="headline"><h1>')
    title_end = con.find(r'</h1></div>',title_initial)
    title = con[title_initial+18:title_end]
    main_initial =  con.find(r'<!content_tag txt>',title_end)
    main_end = con.find(r'<!/content_tag txt></div>',main_initial)
    main =  con[main_initial+18:main_end]
    notice = '转自华尔街日报,版权原因请勿传播'
    notice = notice.decode('utf-8')
    return render_template('post.html',title=title,notice=notice,main=main)

if __name__=='__main__':
    app.debug=True
    app.run()



      
