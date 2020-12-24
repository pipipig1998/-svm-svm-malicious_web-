SVM-基于SVM的恶意域名检测
==========================


安装方法：
----------

 需要在ubuntu中安装libpcap数据包
        
	其次，找到python的安装地址（一般/usr/include/pythonx.x）看是否有Python.h文件。
        
	如果没有，运行sudo apt-get install pythonx.x-dev再寻找

	运行gcc -o xx.o udpget.cpp -I(Python.h)的路径 -lpcap -lpythonx.x
