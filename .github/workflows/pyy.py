import requests
from lxml import etree
import json
from datetime import datetime
from urllib.parse import urljoin
baseurl='http://www.jwc.sjtu.edu.cn/'
url='http://www.jwc.sjtu.edu.cn/index/mxxsdtz.htm'
headers={'User-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
res=requests.get(url,headers=headers)
e=etree.HTML(res.content.decode("UTF-8"))
text=[]
link=[]
#创建初始json
# with open('rec.json','r') as file:
#    text=json.load(file)
with open('record.json','r') as file:
    data=json.load(file)
date3=[]
date4=[]
index=[]
date3=data['date3']
link=data['link']
text=data['text']
index=data['index']
news=e.xpath(f'//*[@id="line_u9_0"]/div[2]/a/h2//text()')
#测试用语句
# text[0]=e.xpath(f'//*[@id="line_u9_3"]/div[2]/a/h2//text()')

if news!=text[0]:
    print (f"新消息，{news}\n最新的通知\n")
    text.clear()
    link.clear()
    date3.clear()
    index.clear()
    for i in range(10):
        news = e.xpath(f'//*[@id="line_u9_{i}"]/div[2]/a/h2//text()')
        text.append(news)
        l=e.xpath(f'//*[@id="line_u9_{i}"]/div[2]//a[1]')
        date1=e.xpath(f'//*[@id="line_u9_{i}"]/div[1]/p//text()')
        date2=e.xpath(f'//*[@id="line_u9_{i}"]/div[1]/h2//text()')
        date = '.'.join([f"{x}.{y}" for x, y in zip(date1, date2)])
        date3.append(date)
        for ele in l:
            ele_url=ele.get('href')
            #ele_url=urljoin(baseurl,ele_url)
            link.append(ele_url)
    sorted_dates = sorted(enumerate(date3), key=lambda x: datetime.strptime(x[1], '%Y.%m.%d'),reverse=True)
    sorted_indices = [index for index, _ in sorted_dates]
    for i in sorted_indices:
        print(date3[i],text[i],'\t',link[i],"\t")
        index.append(i)
    data={'date3':date3,'text':text,'link':link,'index':index}
    with open('record.json', 'w') as file:
        json.dump(data, file)
else :
    print("没有新消息，旧消息为\n")
    for i in index:
        print(date3[i],text[i],'\t',link[i],"\t")
