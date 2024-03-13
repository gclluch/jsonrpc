"""JSON-RPC server implementation."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class JSONRPCException(Exception):
    def __init__(self, code, message, id_):
        self.code = code
        self.message = message
        self.id = id_
        super().__init__(message)


class JSONRPCNotification(Exception):
    """Raised to indicate a JSON-RPC notification."""
    pass


class JSONRPCServer(BaseHTTPRequestHandler):
    """JSON-Rjsonrpc server implementation."""
    methods = {}

    @classmethod
    def register_method(cls, name, method):
        """Register a method to be exposed by the server."""
        if name.startswith('rpc.'):
            raise ValueError("Method names starting with 'rpc.' are reserved for JSON-RPC internal methods and extensions.")
        cls.methods[name] = method

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        response, status_code = self.process_request(post_data)

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def process_request(self, data):
        """Process the JSON-RPC request."""
        try:
            json_data = self.parse_request_data(data)
            self.validate_jsonrpc_version(json_data)
            self.handle_notification(json_data)

            method, params = self.get_method_and_params(json_data)
            result = self.invoke_method(method, params, json_data)
            return self.success_response(result, json_data['id'])
        except JSONRPCException as e:
            return self.error_response(e.code, e.message, json_data.get('id'))

    def parse_request_data(self, data):
        """Parse the request data."""
        try:
            return json.loads(data.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise JSONRPCException(-32700, 'Parse error', None) from e

    def validate_jsonrpc_version(self, json_data):
        """Validate the JSON-RPC version."""
        if json_data.get('jsonrpc') != '2.0':
            raise JSONRPCException(-32600, "Invalid Request: JSON-RPC version must be '2.0'", json_data.get('id'))

    def handle_notification(self, json_data):
        """Handle JSON-RPC notifications."""
        if 'id' not in json_data:
            method_name = json_data.get('method')
            if method_name in self.methods:
                self.methods[method_name](**json_data.get('params', {}))
            raise JSONRPCNotification()

    def get_method_and_params(self, json_data):
        """Get the method and params from the JSON-RPC request."""
        method_name = json_data.get('method')
        if not isinstance(method_name, str):
            raise JSONRPCException(-32600, "Invalid Request: Method name is required and must be a string.", json_data.get('id'))

        method = self.methods.get(method_name)
        if not method:
            raise JSONRPCException(-32601, "Method not found", json_data.get('id'))

        return method, json_data.get('params')

    def invoke_method(self, method, params, json_data):
        """Invoke the method with the given params."""
        if params is None:
            return method()
        elif isinstance(params, list):
            return method(*params)
        elif isinstance(params, dict):
            return method(**params)
        else:
            raise JSONRPCException(-32602, "Invalid params", json_data.get('id'))

    def success_response(self, result, id_):
        """Create a successful JSON-RPC response."""
        return json.dumps({"jsonrpc": "2.0", "result": result, "id": id_}), 200

    def error_response(self, code, message, id_):
        """Create an error JSON-RPC response."""
        return json.dumps({"jsonrpc": "2.0", "error": {"code": code, "message": message}, "id": id_}), 400

def run(
    server_class=HTTPServer,
    handler_class=JSONRPCServer,
    address='',
    port=8000
):
    """Run the JSON-RPC server."""
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()
