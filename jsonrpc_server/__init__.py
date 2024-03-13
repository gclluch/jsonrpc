from .server import JSONRPCServer, run

def register_method(name, method):
    JSONRPCServer.register_method(name, method)