import socket
import sys
from threading import Thread


class TCPServer:
    def __init__(self,host,port):
        self.timeout = 10  # 设置超时时间为10秒
        # 首先尝试连接IPv6地址
        self.serversocket=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.IPPROTO_IPV6,socket.IPV6_V6ONLY,0)
        try:
            self.serversocket.bind((host,port))
        except socket.error:
            self.serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.serversocket.bind((host,port))
        self.serversocket.listen(20)
        print("服务器已连接")

    def do_request(self,clientsocket):
        try:
            r = clientsocket.recv(1024)
            if not r:
                # 处理读取数据的异常
                raise ValueError("接收到了一条空的信息")
        except socket.timeout:
            print("等待客户端数据超时")
        except Exception as e:
            print("An error occurred: {}".format(e))
        data=self.process_request(r) #data 为调用函数后的结果
        try:
            clientsocket.sendall(data.encode('utf-8'))
        except socket.timeout:
            print("发送数据超时")
        except Exception as e:
            print("An error occurred: {}".format(e))
        clientsocket.close()

    def accept_receive_close(self):
        try:
            clientsocket, address = self.serversocket.accept()
            # 为当前连接创建线程
            t = Thread(target=self.do_request, args=(clientsocket,))
            t.start()
        except KeyboardInterrupt:# 按下ctrl+c会触发此异常
            self.serversocket.close()
            sys.exit("\n" + "系统：服务器安全退出！")  # 程序直接退出，不捕捉异常
        except Exception as e:
            print(e)
        # r=clientsocket.recv(1024)
        # data=self.process_request(r)
        # clientsocket.sendall(data.encode('utf-8'))
        # clientsocket.close()