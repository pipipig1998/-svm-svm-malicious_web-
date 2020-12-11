import time
import csv
path=r'./data/datalist/'
def read_website(spath):
    p=path+spath
    print('路径是：',p)
    ml=[]
    with open(p,'r') as f:
        lines=f.readlines()
        for line in lines:
            ml=ml+line.rsplit()
    return ml
def write_sum(sum):
    # t=time.time()
    # s=str(int(t))
    s=path+'m_data'+'.csv'
    with open(s,'w',newline="")as f:
        write=csv.writer(f)
        for i in sum:
            list=[]
            list.append(i)
            write.writerow(list)


if __name__ == '__main__':
    sum=[]
    for i in range(1,6):
        s='0'+str(i)+'.txt'
        # print(s)
        ml=read_website(s)
        # for i in ml:
        #     print(i)
        sum+=ml
    print(len(sum))
    write_sum(sum)
