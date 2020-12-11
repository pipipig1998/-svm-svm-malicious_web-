import requests
import lxml
import re
import time
from bs4 import BeautifulSoup
def get_whois(s):
    url="http://whois.chinaz.com/"+s
    print(url)
    ret = requests.get(url)
    soup = BeautifulSoup(ret.text, 'lxml')
    # ret=soup.select(re.compile('[0-9]*[\u4E00-\u9FA5][0-9]*[\u4E00-\u9FA5][0-9]*[\u4E00-\u9FA5]'))
    ret=soup.select('li>div>span')
    # print(ret)
    list=[]
    r=re.compile('[0-9]*[\u4E00-\u9FA5][0-9]*[\u4E00-\u9FA5][0-9]*[\u4E00-\u9FA5]')
    for i in ret:
        # print(i.string)
        if r.match(i.string)!=None:
            list.append(i.string)
            # print(r.match(i.string))
    if len(list) ==3:
        list.pop(0)
    _l=[]
    for i in list:
        year=i[:4]
        T = (((int(year)-1970)*365 * 24 ) * 60 ) * 60
        _l.append(T)
    return _l[-1]-_l[0]
if __name__ == '__main__':

    print(get_whois('bilibili.com'))