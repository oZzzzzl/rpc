import json

import tcpserver
import threading
class RPCStub:
    def __init__(self):
        self.funcs={}
    def register_function(self,fn,name=None):
        # 方法注册
        if name is None:
            name = fn.__name__
            self.funcs[name] = fn
class JSONRPC:
    def __init__(self):
        self.date=None
    def from_data(self,data):
        self.data=json.loads(data.decode('utf-8'))
    def call(self):
        method_name=self.data.get('method_name', '')
        method_args=self.data.get('method_args', None)
        method_kwargs=self.data.get('method_kwargs', None)
        try:
            if (method_name in self.funcs):
                res=self.funcs[method_name](*method_args, **method_kwargs)
            else:
                res = 'No such method'
            data = {'result': res }
            return json.dumps(data)
        except Exception as e:
            print("An error occurred: {}".format(e))
class RPCServer(tcpserver.TCPServer, JSONRPC, RPCStub):
    def __init__(self,host,port):
        tcpserver.TCPServer.__init__(self, host, port)
        JSONRPC.__init__(self)
        RPCStub.__init__(self)
    def loop(self):
        while True:
            self.accept_receive_close()
    def process_request(self, data):
        self.from_data(data)  # 将来自客户端的请求反序列化
        return self.call()
