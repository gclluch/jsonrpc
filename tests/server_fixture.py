# server_fixture.py

from jsonrpc_server import run, register_method

def sum_numbers(*args, **kwargs):
    # If positional arguments are used
    if args:
        return sum(args)
    # If named arguments are used
    return kwargs['a'] + kwargs['b']

def say_hello(name):
    return f"Hello, {name}!"

def ping():
    return "pong"

# Register methods with the server
register_method('sum', sum_numbers)
register_method('hello', say_hello)
register_method('ping', ping)  # Register the ping method

# This will run the server when the file is executed
if __name__ == "__main__":
    run(address='localhost', port=8000)
