#  coding: utf-8
import socketserver

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
        self.data = self.request.recv(1024).strip()
        print("***************\n" +
              self.data.decode("utf-8").split("\n")[0].split()[1])
        print("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        # self.request.sendall(bytes("Hello World!" + "\r\n", "utf-8"))

        # print(self.request.type)
        # print(dir(self.request))

        msg = "<html><body><h1>This is a test</h1><p>More content here</p></body></html>"

        response_headers = {
            'Content-Type': 'text/html; encoding=utf8',
            'Content-Length': len(msg),
            'Connection': 'close',
        }

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v)
                                       for k, v in response_headers.items())

        response_proto = 'HTTP/1.1'
        response_status = '200'
        response_status_text = 'OK'  # this can be random

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
