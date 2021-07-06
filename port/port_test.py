import os
import time
from scapy.all import *
from optparse import OptionParser
from threading import Thread


def scan(ip,port):
    try:
        packet = IP(dst=ip)/TCP(dport=port, flags="S")  # 构造标志位为syn的数据包
        result = sr1(packet,timeout=0.5, verbose=0)
        if int(result[TCP].flags) == 18:
            # 通过判断响应的数据包中，是否存在第二次握手Ack+syn标志位，存在即端口开放
            time.sleep(0.1)
            print(ip, "TCP" , port, "open")
            # 注意这里如果使用+号进行字符串拼接的话会导致报错，使用逗号即可拼接
        return

    except:
        pass


def main():
    # 如果没有输出参数就会输出帮助信息
    parser = OptionParser("Usage program -i <target host> -n <website> -p <target port>")
    parser.add_option("-i", '--host', type="string",dest="tgtIP",help="specify target host or website")
    parser.add_option("-n","--network", type="string",dest="tgtNetwork",help="specify target Network")
    parser.add_option("-f", "--addressfile", type="string", dest="tgtFile", help="specify target addressfile")
    parser.add_option("-p","--port", type="string",dest="tgtPorts",help="specify target port separated by comma")
    options,args = parser.parse_args()  # 实例化用户输入的参数

    tgtIP = options.tgtIP
    tgtNetwork = options.tgtNetwork # 网段
    tgtFile = options.tgtFile
    tgtPorts = options.tgtPorts
    tgtPorts = tgtPorts.split(",") # 将用户输入的多个端口以逗号分割生成列表

    if tgtPorts is None or tgtNetwork is None and tgtIP is None and tgtFile is None  :  # 判断用户是否输入参数
        print(parser.usage) # 如果没有输入参数则输出帮助信息，然后退出程序
        exit(0)
       
   

    if tgtIP:   # 输入单个ip地址时的操作
        for p in tgtPorts:
            port = int(p)
            t = Thread(target=scan,args=(tgtIP,port))
            t.start()

    if tgtNetwork:  # 输入整个网段时的操作
        prefix = tgtNetwork.split(".")[0] + "." + tgtNetwork.split(".")[1] + "." + tgtNetwork.split(".")[2] + "."   # 将用户输入的网段提取提取前三位当作前缀
        for i in range(1,255):
            ip = prefix + str(i)    # 和前缀结合形成网段内所有的地址
            for p in tgtPorts:
                port = int(p)
                t = Thread(target=scan, args=(ip,port))
                t.start()



    if tgtFile: # 如果时地址文件则进行的操作
        if not os.path.exists(tgtFile):     # 判断文件是否存在
            print("File not found")
            sys.exit()
        with open(tgtFile,"r") as f:    # 读取地址文件
            for i in f.readlines():
                ip = i.strip()      # 读取用户地址文件的地址，并去点换行空格
                for p in tgtPorts:
                    port = p.strip()
                    port = int(port)   
                    t = Thread(target=scan,args=(ip,port))
                    t.start()   # 多线程扫描


if __name__ == '__main__':
    print("start")
    main()