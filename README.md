SVM-基于SVM的恶意域名检测
==========================


安装方法：
----------


 	需要在ubuntu中安装libpcap数据包
        
	其次，找到python的安装地址（一般/usr/include/pythonx.x）看是否有Python.h文件。
        
	如果没有，运行sudo apt-get install pythonx.x-dev再寻找

	运行gcc -o xx.o udpget.cpp -I(Python.h)的路径 -lpcap -lpythonx.x
	
  例如：我的在/usr/include/python3.6 则运行gcc -o test.o udpget.cpp -I/usr/include/python3.6 -lpython3.66 -lpcap
  

说明：
-----

  1.pickle是SVM训练后的结果
  
  Mycall是调用python，实现判断域名好坏，保存数据库
  
  udpget是利用libpcap进行捕获包
  
  
思路：
-----
  udpget.cpp捕获包然后传给Mycall.py，如果运行的时候数据库已经

  保存了相关的域名

  结果，则返回空，输出failed method 
