#!/usr/bin/env python3
"""
Collects temperature / gravity readings from Spindel

start standalone with sudo python3 spindel_server.py 85
test with curl -d "{\"temperature\":12,\"angle\":10,\"gravity\":121212}" ip:port

"""
import socketserver
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from db import Logger
import configparser
import requests
import os


def get_config(config_file):
    config_input = configparser.ConfigParser()
    config_input.read(config_file)

    config = dict()

    config['PUSH_ENDPOINT'] = config_input.get('holdmybeer', 'collection_endpoint')
    config['PUSH_API_KEY'] = config_input.get('holdmybeer', 'apikey')

    return config


def post_data(url, apikey, body):
    headers = {'content-type': 'application/json', 'x-api-key': apikey}
    requests.post(url, data=json.dumps(body), headers=headers)


def RequestHandlerFactory(logger, config_file):
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

            try:
                config = get_config(config_file)
                target_endpoint = config.get('PUSH_ENDPOINT')
                target_apikey = config.get('PUSH_API_KEY')
                print('forwarding payload to', target_endpoint)
                post_data(target_endpoint, target_apikey, parsed_body)
            except:
                print('failed while posting data to remote server')

    return S


def spindel_server(logger, config_file, port=80):
    request_handler = RequestHandlerFactory(logger, config_file)
    server_address = ('', port)
    httpd = HTTPServer(server_address, request_handler)
    print('Starting httpd...')
    httpd.serve_forever()


# run the server on its own, useful for debugging
if __name__ == "__main__":
    logger = Logger('test')
    config_file = os.path.dirname(
        os.path.realpath(__file__)) + "/config.ini"
    spindel_server(logger, config_file, port=int(sys.argv[1]))
