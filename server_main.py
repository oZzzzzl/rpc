import socket
import json
import sys
import time
from threading import Thread
import rpcserver
import sys
import local_function as lf
isAlive=True
def register_func(s, conn, fn, host, port, name=None):
    # 注册函数信息到注册中心
    if name is None:
        name = fn.__name__
    msg={'identity': 'server',
         'name':name,
         'ip':str(host),
         'port':str(port)
         }
    #msg='server'+'name'+name+'ip'+str(host)+'port'+str(port)
    conn.sendall(json.dumps(msg).encode('utf-8'))
    print(msg['name']+'已提交注册申请')
    response_msg = conn.recv(1024)
    response_msg = json.loads(response_msg.decode('utf-8'))
    print(response_msg+'已成功注册')
    #讲函数登记在本地表便于调用
    s.register_function(fn)

def do_register_request(conn,host,port):
    idt = {
        'ip': str(host),
        'port': str(port)
    }
    # print(json.dumps(idt).encode('utf-8'))
    conn.sendall(json.dumps(idt).encode('utf-8'))  # 向注册中心表面身份
    # 注册函数
    time.sleep(0.1)  # 发送完idt不sleep一会好像会粘包
    register_func(s, conn, lf.test, host, port)
    register_func(s, conn, lf.add_num, host, port)
    register_func(s, conn, lf.sub_num, host, port)
    register_func(s, conn, lf.func1, host, port)
    register_func(s, conn, lf.func2, host, port)
    register_func(s, conn, lf.func3, host, port)
    register_func(s, conn, lf.func4, host, port)
    register_func(s, conn, lf.func5, host, port)
    register_func(s, conn, lf.func6, host, port)
    register_func(s, conn, lf.func7, host, port)
def do_user_request(conn):
    # 用于接收用户输入参数
    # print("若想中止该服务器的运行，请输入-exit")
    while True:
        msg=input()
        if msg=='exit':
            # 用户主动希望该服务器退出
            conn.sendall(json.dumps(msg).encode('utf-8'))  # 向注册中心表面自己需要断开
            conn.close()
            break
    global isAlive
    isAlive=False
    sys.exit()
def send_heartbeat(conn,host,port):
    global isAlive
    while True:
        time.sleep(0.5)
        # 向注册中心发送心跳证明存活
        msg = {'identity': 'server',
                'name': 'I am alive!',
                'ip': str(host),
                'port': str(port)
                }
        if isAlive:
            # msg='server'+'name'+name+'ip'+str(host)+'port'+str(port)
            conn.sendall(json.dumps(msg).encode('utf-8'))
        else:
            sys.exit()
def start_server(s):
    s.loop()

if __name__ == '__main__':
    value=sys.argv[1]
    if value=='-h':
        print("启动参数为: -l ip地址 -p 端口号")
        sys.exit()
    value1=sys.argv[2]
    value2=sys.argv[4]
    host=value1
    port=int(value2)
    s=rpcserver.RPCServer(host,port)#启动服务器
    print("服务器已启动，输入exit可退出服务器")
    #注册中心的地址
    rc_addr='192.168.33.236'
    rc_port=6000
    conn_register = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_register.connect((rc_addr,rc_port))
    # 连接注册中心并注册函数
    t = Thread(target=do_register_request, args=(conn_register,host,port))
    t.start()

    # 创建一个线程来不断向注册中心发送心跳
    t1 = Thread(target=send_heartbeat, args=(conn_register, host, port))
    t1.daemon = True  # 设置为守护线程，这样主线程结束时，子线程也会结束
    t1.start()
    #conn_register.sendall(json.dumps('exit').encode('utf-8'))
    #处理客户端请求
    t2=Thread(target=start_server,args=(s,))
    t2.daemon= True
    t2.start()
    #s.loop()

    # 该线程用于处理用户输入
    t3=Thread(target=do_user_request, args=(conn_register,))
    t3.start()
    #当用户主动退出时
    while True:
        time.sleep(0.5)
        if not isAlive:
            print('Server stopped')
            break