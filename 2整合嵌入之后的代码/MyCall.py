from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
import re
import requests
from bs4 import BeautifulSoup
import pickle
import pymysql
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
    year=list[0][:4]
    _l=[]
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
def display(x):
        l,c,e=num_percent(x)
        t=get_whois(x)
        #print(l,c,e,t)
        list=[l,c,e,t]
        return list
def connection(url,src_ip,sport,dst_ip,dport,judge):
    # (url, src_ip, sport, dst_ip, dport, judge)
    conn = pymysql.connect('localhost', 'root', 'toor')
    conn.select_db('web_dns')
    cur = conn.cursor()

    sql="insert into store(url,src_ip,src_sport,dst_ip,dst_sport,judge) values(%s,%s,%s,%s,%s,%s)"
    print(url,src_ip,sport,dst_ip,dport,judge)
    cur.execute(sql,(url,src_ip,sport,dst_ip,dport,judge))

    cur.close()
    conn.commit()
    conn.close()
    print('sql执行成功')
def My_Funct(s,sport,dport,src_ip1,src_ip2,src_ip3,src_ip4,dst_ip1,dst_ip2,dst_ip3,dst_ip4):
    src_ip=str(src_ip1)+"."+str(src_ip2)+"."+str(src_ip3)+"."+str(src_ip4)
    dst_ip=str(dst_ip1)+"."+str(dst_ip2)+"."+str(dst_ip3)+"."+str(dst_ip4)
    clf=None
    with open('1.pickle','rb') as f:
        clf=pickle.load(f)
    #print("get",s)
    s=s[:-1]
    print("url %s,src_ip %s,dst_ip %s,src_port %s,dst_port %s"%(s,src_ip,dst_ip,sport,dport))
    s=s.split('.')
   # print(s)
    url=s[-2]+"."+s[-1]
   # print(url)
    l=display(url)
    b = np.array(l)
    judge=None
    if clf.predict([b])[0]== 1:
        judge='bad'
    else:
        judge='good'
    url=""
    for i in s:
        url=url+i+"."
    url=url[:-1]
    connection(url,src_ip,sport,dst_ip,dport,judge)
    
if __name__ == '__main__':
    s=input()
    print(My_Funct("qq.com.",55,66,1,2,3,4,1,2,3,4))

