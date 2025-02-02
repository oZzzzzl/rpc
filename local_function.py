def test(*args, **kwargs):
    print("test被调用")
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key} = {value}")
def add_num(*args, **kwargs):
    print("add_num被调用")
    if args[0] is None or args[1] is None:
        raise ValueError("参数错误")
    #print(args[0],args[1])
    return int(args[0])+int(args[1])
def sub_num(*args, **kwargs):
    print("sub_num被调用")
    if args[0] is None or args[1] is None:
        raise ValueError("参数错误")
    return int(args[0]) - int(args[1])
def func1(*args, **kwargs):
    print("func1被调用")
    if args[0] is None or args[1] is None or args[2] is None:
        raise ValueError("参数错误")
    return (int(args[0]) - int(args[1]))*int(args[2])
def func2(*args, **kwargs):
    print("func2被调用")
    if args[0] is None or args[1] is None or args[2] is None:
        raise ValueError("参数错误")
    return int(args[2])+int(args[1])*int(args[0])
def func3(*args, **kwargs):
    print("func3被调用")
    if args[0] is None or args[1] is None:
        raise ValueError("参数错误")
    return int(args[1])*int(args[1])*int(args[0])
def func4(*args, **kwargs):
    print("func4被调用")
    if args[0] is None or args[1] is None or args[2] is None:
        raise ValueError("参数错误")
    return (int(args[1])+int(args[1]))%2+int(args[2])
def func5(*args, **kwargs):
    print("func5被调用")
    if args[0]:
        raise ValueError("参数错误")
    return int(args[0])*int(args[0])
def func6(*args, **kwargs):
    print("func6被调用")
    if args[0] is None or args[1] is None:
        raise ValueError("参数错误")
    return float(args[0])+float(args[1])
def func7(*args, **kwargs):
    print("func7被调用")
    if args[0] is None or args[1] is None or args[2] is None:
        raise ValueError("参数错误")
    return int(args[1])*int(args[2])*int(args[1])*int(args[0])

