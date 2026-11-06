import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from second_draft import App, make_request


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.server.path_seen = self.path
        self.server.payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.server.auth = self.headers.get('Authorization')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'choices': [{'message': {'content': 'The rain arrived before dawn.'}, 'finish_reason': 'stop'}]}).encode())

    def log_message(self, *args):
        pass


class ApiTests(unittest.TestCase):
    def test_generation_round_trip(self):
        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            request = make_request('http://127.0.0.1:%s/v1' % server.server_port, 'test-key', 'host/model', 'A stranger arrives.', 'Spare prose.', 'Rain on the road.')
            app = App.__new__(App)
            app.fetch(request)
            self.assertEqual(app.result, (True, 'The rain arrived before dawn.', False))
            self.assertEqual(server.path_seen, '/v1/chat/completions')
            self.assertEqual(server.auth, 'Bearer test-key')
            self.assertEqual(server.payload['model'], 'host/model')
            for reference in ['A stranger arrives.', 'Spare prose.', 'Rain on the road.']:
                self.assertIn(reference, server.payload['messages'][1]['content'])
        finally:
            server.shutdown()
            thread.join()
            server.server_close()

    def test_validation(self):
        for endpoint, model, outline in [('http://example.com/v1', 'model', 'outline'), ('https://example.com/v1', '', 'outline'), ('https://example.com/v1', 'model', '')]:
            with self.assertRaises(ValueError):
                make_request(endpoint, '', model, outline, '', '')

    def test_connection_failure_preserves_result_contract(self):
        app = App.__new__(App)
        app.fetch(make_request('http://127.0.0.1:1/v1', '', 'model', 'outline', '', ''))
        self.assertFalse(app.result[0])


if __name__ == '__main__':
    unittest.main()
