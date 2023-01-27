#  coding: utf-8
import socketserver
from pathlib import Path
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        error = False
        method_not_allowed = False
        redirect = False

        self.data = self.request.recv(1024).strip()

        print("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        # self.request.sendall(bytes("Hello World!" + "\r\n", "utf-8"))

        # print(self.request.type)
        # print(dir(self.request))
        first_line_request = self.data.decode("utf-8").split("\n")[0].split()
        print(first_line_request)

        method = first_line_request[0]

        if method != "GET":
            method_not_allowed = True

        print("************ Method: ", method)

        decoded_path = self.data.decode("utf-8").split("\n")[0].split()[1]

        path = Path(r'{}'.format(decoded_path))

        # Directory and missing the path ending
        if os.path.isdir(f"www{path}") and not decoded_path.endswith("/"):
            # Redirect
            redirect = True

        # parent = path.parent
        name = str(path.name)
        suffix = str(path.suffix)

        print("Path: *************** " + str(path))
#
        # if path == "/":
        #     file = open("www/index.html")
        #     msg = file.read()
        # else:
        msg = "<html><body><h1>This is a test</h1><p>More content here</p></body></html>"

        print("^^^^^^^^ " + name)
        if len(name) == 0 or len(suffix) == 0:
            concat_path = "www" + str(path) + "/" + "index.html"
            print("**********" + concat_path)
            try:
                file = open(concat_path)
                msg = file.read()
            except:
                error = True
        else:
            try:
                file = open("www" + str(path))
                msg = file.read()
            except:
                error = True
        # file = None
        # if path == "/":
        #     file = open(f"www{path}/index.html")
        #     msg = file.read()
        if error:
            msg = "404 Not Found"
        elif method_not_allowed:
            msg = "405 Method Not Allowed"
        elif redirect:
            msg = "301 Moved Permanently"

        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(msg),
            'Connection': 'close',
        }

        if suffix.endswith("css"):
            response_headers['Content-Type'] = 'text/css; encoding=utf8'

        if redirect:
            response_headers['Location'] = f'{decoded_path}/'

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v)
                                       for k, v in response_headers.items())

        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'  # this can be random

        if error:
            response_status = '404'
            response_status_text = 'Not Found'
        elif method_not_allowed:
            response_status = '405'
            response_status_text = 'Method Not Allowed'
        elif redirect:
            response_status = '301'
            response_status_text = 'Moved Permanently'

        r = '%s %s %s\r\n' % (
            response_proto, response_status, response_status_text)
        self.request.send(bytes(r, "utf-8"))
        self.request.send(bytes(response_headers_raw, "utf-8"))
        self.request.send(bytes("\r\n", "utf-8"))
        self.request.send(bytes(msg, "utf-8"))

        # print(r)
        # print(response_headers_raw)

        # print(msg)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
