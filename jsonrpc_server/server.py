from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class JSONRPCServer(BaseHTTPRequestHandler):
    methods = {}

    @classmethod
    def register_method(cls, name, method):
        cls.methods[name] = method

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        response, status_code = self.process_request(post_data)

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

    def process_request(self, data):
        try:
            json_data = json.loads(data.decode('utf-8'))
            method_name = json_data.get('method')
            params = json_data.get('params', [])
            method = self.methods.get(method_name)

            if not method:
                return json.dumps({"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": json_data.get('id')}), 404

            result = method(*params) if isinstance(params, list) else method(**params)
            return json.dumps({"jsonrpc": "2.0", "result": result, "id": json_data.get('id')}), 200
        except Exception as e:
            return json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}, "id": json_data.get('id')}), 400

def run(server_class=HTTPServer, handler_class=JSONRPCServer, address='', port=8000):
    server_address = (address, port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()
