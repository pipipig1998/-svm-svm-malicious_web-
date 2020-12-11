import time
import csv
path=r'./data/datalist/'
def read_website():
    sum = []
    with open(path+'11.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.split('/')
            sum.append(line[1])
    return sum
def write_website(sum):
    t=int(time.time())
    t=str(t)
    print(t)
    with open(path++'w_data.csv','w',newline="")as f:
        write=csv.writer(f)
        for item in sum:
            print(item)
            line=[]
            line.append(item)
            print(line)
            write.writerow(line)
if __name__ == '__main__':
    sum=read_website()
    write_website(sum)