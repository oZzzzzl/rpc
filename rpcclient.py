import json
import tcpclient
class RPCStub:
    def __getattr__(self, item):
        def func(*args, **kwargs):
            d = {
                'method_name':args[0],
                'method_args':args[1],
                'method_kwargs':kwargs,
            }
            self.send(json.dumps(d))  #发送数据到服务器
            return self.receive(1024)  #接收服务器结果
        setattr(self,item,func)
        return func

class RPCClient(tcpclient.TCPClient,RPCStub):
    pass