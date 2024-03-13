from .server import JSONRPCServer, run

def register_method(name, method):
    """Register a method to be exposed by the JSON-RPC server."""
    JSONRPCServer.register_method(name, method)