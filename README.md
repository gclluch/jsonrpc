# JSON-RPC Server for Python

A lightweight, easy-to-use JSON-RPC 2.0 server implementation in Python, designed for simplicity and minimal dependencies. This package allows you to quickly set up a JSON-RPC server to handle remote procedure calls in a standardized way, supporting both single and batch requests.

## Features

- Simple and straightforward JSON-RPC 2.0 compliance.
- Supports method registration for handling RPC calls.
- Handles single and batch requests.
- Built-in support for notifications (requests without response).
- Easy integration into existing Python applications.

## Installation

To install the JSON-RPC Server, simply use pip:

```bash
pip install git+https://github.com/gclluch/jsonrpc-server.git
```

## Quick Start

Define the methods you want to expose through JSON-RPC, register your methods with the server, and run the server


```python
from jsonrpc_server import register_method, run

def add(a, b):
    return a + b

register_method('add', add)

if __name__ == "__main__":
    run(address='localhost', port=8000)
```


## Example

Request: 

```bash
{
  "jsonrpc": "2.0",
  "method": "add",
  "params": [1, 2],
  "id": 1
}
```

Result:

```bash
{
  "jsonrpc": "2.0",
  "result": 3,
  "id": 1
}
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to improve the project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.