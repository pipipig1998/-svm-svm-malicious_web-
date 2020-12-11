from sklearn import svm
import numpy as np
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt
import matplotlib
if __name__ == '__main__':
    path='./data/datalist/m_feature.csv'
    data=np.loadtxt(fname=path,dtype=float,delimiter=',')
    # print(type(data))#np.array
    x,y=np.split(data,indices_or_sections=(4,),axis=1)
    train_data,test_data,train_label,test_label=train_test_split(x,y,train_size=0.5,test_size=0.5)
    classfier=svm.SVC(C=0.39,kernel='rbf',gamma=0.02,decision_function_shape='ovo')
    classfier.fit(train_data,train_label.ravel())
    print("训练集：",classfier.score(train_data,train_label))
    print("测试集：",classfier.score(test_data,test_label))
    # print('train_decision_function:\n', classfier.decision_function(train_data))  # (90,3)
    # print('predict_result:\n', classfier.predict(train_data))
    # print('这是训练数据:',test_data)
    with open('1.pickle','wb') as f:
        pickle.dump(classfier,f)