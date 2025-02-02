import socket
import json
class TCPClient:
    def __init__(self,host,port):
        self.timeout = 5  # 设置超时时间为5秒
        # 首先尝试连接IPv6地址
        client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        client_socket.settimeout(self.timeout)
        try:
            client_socket.connect((host, port))
        except socket.timeout:
            print("Connection timed out") #超时处理
        except socket.error:
            # 如果IPv6连接失败，尝试连接IPv4地址
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(self.timeout)
            try:
                client_socket.connect((host, port))
            except socket.timeout:
                print("连接超时")  # 超时处理
        except Exception as e:
            print("An error occurred: {}".format(e))
        self.clientsocket = client_socket

    def send(self,data):
        try:
            self.clientsocket.sendall(data.encode('utf-8'))
        except socket.timeout:
            print("发送超时")
        except Exception as e:
            print("An error occurred: {}".format(e))

    def receive(self,length):
        try:
            r=self.clientsocket.recv(length)
            r=r.decode('utf-8')
            r=json.loads(r)
            return r
        except socket.timeout:
            print("等待响应超时")
        except Exception as e:
            print("An error occurred: {}".format(e))