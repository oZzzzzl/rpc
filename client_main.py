import socket
import rpcclient
import sys
from rpcclient import *

def connect_to_register_center():
    # 连接注册中心并查询函数
    #rc_addr='127.0.0.1'
    rc_addr='192.168.33.236'
    rc_port=6000
    conn_register = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn_register.connect((rc_addr, rc_port))
    conn_register.sendall(json.dumps('client').encode('utf-8'))  # 向注册中心表面自己的客户端身份
    receive_list = conn_register.recv(1024)
    receive_list = json.loads(receive_list.decode('utf-8'))
    print("当前可调用函数有" + str(receive_list))
    return conn_register
def procedure_start():
    if sys.argv[1] == '-h':
        print("输入-s启动客户端")
        sys.exit()
    elif sys.argv[1] != '-s':
        print("请输入正确的启动参数")
        sys.exit()
def loop(conn_register):
    while True:
        func_name = input("请输入你需要调用的函数名(输入exit以结束查询)：")
        if func_name == "exit":
            conn_register.sendall(json.dumps(func_name).encode('utf-8'))
            break
        msg={'identity':'client',
             'name':str(func_name)}
        conn_register.sendall(json.dumps(msg).encode('utf-8'))
        response_msg = conn_register.recv(1024)
        response_msg = json.loads(response_msg.decode('utf-8'))
        if not response_msg == str(func_name)+'不存在任何服务器中':
            #print(response_msg)
            print('查询到该函数所在服务器的IP与端口号为' + str(response_msg))
            addr = response_msg['addr']
            port = int(response_msg['port'])
            c=rpcclient.RPCClient(addr,port)#与目的服务器连接
            arguments = []
            # 提示用户输入数据，并使用循环来收集输入
            while True:
                input_str = input('请一个个输入函数的参数,输入exit来结束')
                if input_str.lower() == 'exit':  # 假设用户输入exit来停止输入
                    break
                arguments.append(input_str)  # 将输入添加到列表中
            res=c.use_func(func_name,arguments)
            if not res:
                # 如果接收到的数据为空，抛出异常
                raise ValueError("客户端收到了一个空结果")
            print("远程调用的返回值 res = {}".format(res))
        else:
            print(response_msg)
if __name__ == '__main__':
    procedure_start()
    conn_register=connect_to_register_center()
    loop(conn_register)



