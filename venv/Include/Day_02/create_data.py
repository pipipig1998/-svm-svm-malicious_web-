import csv
import  whois
import datetime
import time
import requests
from bs4 import BeautifulSoup
import re
path=r'./data/datalist/'
c_list=[
    'b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','chi','sh','r','z','c',
    's','y','w'
]
e_list=[
    'a','e','i','o','u'
]
num_list=[
    '0','1','2','3','4','5','6','7','8','9'
]
f_ls=[]
def read(s):
    sum=[]
    with open(path+s,'r') as f:
        reader=csv.reader(f)
        for row in reader:
            sum+=row
    return sum
def get_level(s):
    if s=='com' or s=='org' or s=='net' or s=='edu':
        return 1
    else:
        return 0
def get_whois(s):
    url="http://whois.chinaz.com/"+s
    print(url)
    ret = requests.get(url)
    soup = BeautifulSoup(ret.text, 'lxml')
    # ret=soup.select(re.compile('[0-9]*[\u4E00-\u9FA5][0-9]*[\u4E00-\u9FA5][0-9]*[\u4E00-\u9FA5]'))
    ret=soup.select('li>div>span')
    # print(ret)
    list=[]
    r=re.compile('[0-9]+[\u4E00-\u9FA5][0-9]+[\u4E00-\u9FA5][0-9]+[\u4E00-\u9FA5]')
    for i in ret:
        # print(i.string)
        if r.match(i.string)!=None:
            list.append(i.string)
            # print(r.match(i.string))
    if len(list)<=0:
        return 0
    if len(list) >=3:
        for i in list:
            if r.match(i)==None:
                list.remove(i)
    list.sort()
    # print(list)
    _l=[]
    print(list)
    year=list[0][:4]
    print("年是:",year)
    T = (((2020-int(year))*365 * 24 ) * 60 ) * 60
    _l.append(T)
    return _l[0]
def num_percent(s):#特征：长度，数字占比，中文单音节字母占比，英文元音占比,域名
    list=s.split('.')
    length=0
    ans_num=0
    ans_c=0
    ans_e=0
    domain=None
    if len(list)==1:
        domain=None
        length=len(list[0])
        for i in list[0]:
            if i in num_list:
                ans_num+=1
            elif i in c_list:
                ans_c+=1
            elif i in e_list:
                ans_e+=1
    else:
        domain=list[-1]
        list=list[:len(list)-1]
        for _s in list:
            length+=len(_s)
            for i in _s:
                if i in num_list:
                    ans_num+=1
                elif i in c_list:
                    ans_c+=1
                elif i in e_list:
                    ans_e+=1
    if length == 0:
        length=1e9
        ans_num=1e9
    return length,ans_c/length,ans_e/length
# def get_whois(s):
#     try:
#         data = whois.query(s)
#         start = data['creation_date']
#         start = time.mktime(start[0].timetuple())
#         end = data['expiration_date']
#         end = time.mktime(end[0].timetuple())
#         now = datetime.datetime.now()
#         now = time.mktime(now.timetuple())
#         time.sleep(5)
#     except Exception:
#         print("whois信息获取不到,当前的网站是：",s)
#         start=0
#         now=0
#         end=0
#     return now-start
def display(x,flag):
    ans=0
    with open(path + 'm_feature.csv', 'a',newline="")as f:
        write = csv.writer(f)
        for i in x:
            ans+=1
            print("第%d个"%ans)
            # print(i)
            l,c,e=num_percent(i)
            t=get_whois(i)
            if(t==0):
                f_ls.append(i)
            print(l,c,e,t)
            list=[l,c,e,t,flag]
            write.writerow(list)
if __name__ == '__main__':
    ml=read('m_data.csv')
    wl=read('w_data.csv')
    print(type(ml))
    for i in f_ls:
        print(i)

    display(wl,-1)
    display(ml,1)
    # get_whois('sina.com.cn')