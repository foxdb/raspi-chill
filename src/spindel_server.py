#!/usr/bin/env python3
"""
Collects temperature / gravity readings from Spindel

test with curl -d "{\"temperature\":12,\"angle\":10,\"gravity\":121212}" ip:port

"""
import socketserver
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from db import Logger


def RequestHandlerFactory(logger):
    class S(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            self.wfile.write("<html><body>ACK</body></html>")

        def do_HEAD(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        def handle_http(self, status_code, path):
            self.send_response(status_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            content = 'thanks'
            return bytes(content, 'UTF-8')

        def respond(self, opts):
            response = self.handle_http(opts['status'], self.path)
            self.wfile.write(response)

        def do_POST(self):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            # this is very fragile, add some error handling: parsing body, and accessing temp, gravity and angle
            # works for the Spindel payload though.

            print('POST: body: ' + body.decode('utf-8'))
            logger.writeRawSpindel(body)

            self.respond({'status': 200})

            parsed_body = json.loads(body.decode('utf-8'))

            print('Parsed: ', parsed_body)
            logger.writeInternalTemperature(parsed_body['temperature'])
            logger.writeAngle(parsed_body['angle'])
            logger.writeGravity(parsed_body['gravity'])

    return S


def spindel_server(logger, port=80):
    request_handler = RequestHandlerFactory(logger)
    server_address = ('', port)
    httpd = HTTPServer(server_address, request_handler)
    print('Starting httpd...')
    httpd.serve_forever()


# run the server on its own, useful for debugging
if __name__ == "__main__":
    logger = Logger('test')
    spindel_server(logger, port=int(sys.argv[1]))
