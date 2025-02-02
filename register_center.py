import socket
import json
import sys
import time
import random
from threading import Thread
funcs = {} # 用于存储（函数名，IP）映射
server_alive={} #用于监测某服务器是否存活
def register_function(name,addr,port):
    # 方法注册
    entry={'addr':addr,'port':port}
    if name in funcs:
        funcs[name].append(entry)
    else:
        funcs[name]=[{'addr':addr,'port':port}]
    print('来自'+str(entry)+'的'+name+'已注册')

def get_type(msg):
    # 判断信息是来自服务器还是客户端
    return msg['identity']
def load_balance(addr):
    # 随机
    return random.choice(addr)
def func_search(name):
    # 根据函数名查找，返回目标服务器的IP和端口
    if name in funcs.keys():
        res=funcs[name]
        return load_balance(res)
    else:
        return None

def delete_server(addr,port):
    # 删除map中的这些键值对
    tmp={'addr':addr,'port':port}
    for name,ids in list(funcs.items()):
        if tmp in ids:
            ids.remove(tmp)
            if not ids:
                #该函数名的值已被删完
                del funcs[name]
    print(funcs)
def heart_handle(addr,port):
    while True:
        # 每隔1s进行一次存活监测
        time.sleep(1)
        if server_alive[(addr,port)] == True:
            server_alive[(addr, port)]=False
        elif(server_alive[(addr, port)]==False):
            print((addr,port),'检测不到心跳，已断开')
            #把该服务器的服务从表中删除
            delete_server(str(addr),str(port))
            break
def do_request(clientsocket,addr,port):
    if addr != None and port != None:
        #创建一个线程，用于定时监测该服务器是否存活
        t = Thread(target=heart_handle,args=(addr,port))
        t.start()
    while True:
        r = clientsocket.recv(1024)
        # 把接收的函数名-IP、端口信息反序列化
        try:
            # 假设 r 是你从某个网络请求中获得的 bytes 类型的响应体
            decoded_response = r.decode('utf-8')
            if decoded_response:  # 确保响应体不为空
                msg = json.loads(decoded_response)
            else:
                print("Received an empty response.")
        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            # 这里你可以添加额外的错误处理逻辑，比如重试请求或记录日志

        #print(msg)
        if msg == 'exit':
           print('有客户端断开连接')
           clientsocket.close()
           break
        identity= get_type(msg)
        if identity == 'server':
            if msg['name'] == 'I am alive!':
                # 假如接收到的是来自于服务器的心跳
                server_alive[(msg['ip'],msg['port'])] = True
            else:
                # 假如接收到的是服务器的注册信息
                name=msg['name']
                addr=msg['ip']
                port=msg['port']
                #name, addr, port = spilt_msg(body_msg)
                register_function(name, addr, port)
                #print(funcs)
                response_msg = name + "已注册"
                clientsocket.sendall(json.dumps(response_msg).encode('utf-8'))
        elif identity == 'client':
            addr=func_search(msg['name'])
            if addr is not None:
                clientsocket.sendall(json.dumps(addr).encode('utf-8'))
            else:
                response_msg = str(msg['name'])+'不存在任何服务器中'
                clientsocket.sendall(json.dumps(response_msg).encode('utf-8'))

def create_socket():
    #host="::"
    #host='192.168.33.236'
    host=socket.gethostbyname(socket.gethostname())
    port=6000
    #serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #serversocket.setsockopt(socket.IPPROTO_IPV6,socket.IPV6_V6ONLY,0)
    serversocket.bind((host, port))
    serversocket.listen(20) # 设置服务器接受的链接数量
    return serversocket
if __name__ == '__main__':
    serversocket = create_socket()
    while True:
        try:
            # 接收来自服务端的连接
            clientsocket, address = serversocket.accept()
        except Exception as e:
            print(e)
            continue

        #识别身份
        r = clientsocket.recv(1024)
        msg = json.loads(r.decode('utf-8'))
        if msg=='client':  #若msg来自客户端，内容则为'client'，若是服务器，则是ip+端口
            # 为当前连接创建线程
            t = Thread(target=do_request, args=(clientsocket,None,None))
            t.start()
            # 向客户端发送当前可调用函数列表
            keys_list = [key for key in funcs.keys()]
            clientsocket.sendall(json.dumps(keys_list).encode('utf-8'))
        else:
            #若为服务器
            addr = msg['ip']
            port = msg['port']
            server_alive[(addr,port)] = True  #登记，表明存活
            # 为当前连接创建线程
            t = Thread(target=do_request, args=(clientsocket,addr,port))
            t.start()
        # t = Thread(target=do_request, args=(clientsocket,'127.0.0.1',5000))
        # t.start()
