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


def is_not_directory_traversal(path):
    safe_path = '/www/'

    # /www/ or /www + / s
    if (os.path.realpath(path).startswith(safe_path)) or (f"{os.path.realpath(path)}/" == safe_path):
        return True
    else:
        return False


def build_message_and_response(status, identifier):
    status_codes = {
        200: "OK",
        301: "Moved Permanently",
        404: "Not Found",
        405: "Method Not Allowed"
    }
    if identifier == "message":
        return f"{status} {status_codes[status]}"
    elif identifier == "response":
        return 'HTTP/1.1', str(status), status_codes[status]


def build_response_headers(msg, suffix, status, decoded_path):
    response_headers = {
        'Content-Type': 'application/octet-stream; charset=utf-8',
        'Content-Length': len(msg),
        'Connection': 'close',
    }
    if suffix.endswith("html"):
        response_headers['Content-Type'] = 'text/html; charset=utf-8'

    elif suffix.endswith("css"):
        response_headers['Content-Type'] = 'text/css; charset=utf-8'

    if status == 301:
        response_headers['Location'] = f'{decoded_path}/'

    # Invalid file or invalid directory, show an HTML error message
    if (suffix and status == 404) or (not suffix and status == 404):
        response_headers['Content-Type'] = 'text/html; charset=utf-8'

    return response_headers


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):

        status = 200

        self.data = self.request.recv(1024).strip()

        # print ("Got a request of: %s\n" % self.data)

        # ['GET', '/', 'HTTP/1.1']
        first_line_request = self.data.decode("utf-8").split("\n")[0].split()

        # Check if the GET /path HTTP/1.1 exists
        try:
            http_method = first_line_request[0]
        except:
            http_method = None

        # Check if the GET /path HTTP/1.1 exists
        try:
            decoded_path = first_line_request[1]
        except:
            decoded_path = '/'

        path = Path(r'{}'.format(decoded_path))

        # Only allow GET requests
        if http_method != "GET":
            status = 405

        # Directory and missing the path ending
        elif is_not_directory_traversal(f"/www{path}") and os.path.isdir(f"www{path}") and not decoded_path.endswith("/"):
            # Redirect
            status = 301

        # Directory, serve index or index.html
        elif is_not_directory_traversal(f"/www{path}") and os.path.isdir(f"www{path}"):
            concat_path = f"www{path}/index.html"
            path = Path(r'{}'.format(concat_path))
            try:
                file = open(path)
                msg = file.read()
            except:
                status = 404
            else:
                file.close()

        # File, serve the file
        elif is_not_directory_traversal(f"/www{path}") and os.path.isfile(f"www{path}"):
            try:
                file = open(f"www{path}")
                msg = file.read()
            except:
                status = 404
            else:
                file.close()

        # Not a directory or a file
        else:
            status = 404

        # print(status)
        # print(path.suffix)

        # Show the error message in HTML if suffix is an empty string
        # suffix = str(path.suffix) if str(path.suffix) else ".html"
        suffix = str(path.suffix)

        if status != 200:
            msg = build_message_and_response(status, "message")

        response_headers = build_response_headers(
            msg, suffix, status, decoded_path)

        response_headers_raw = ''.join('%s: %s\r\n' % (k, v)
                                       for k, v in response_headers.items())

        # print(response_headers_raw)

        response_protocol, response_status, response_status_text = build_message_and_response(
            status, "response")

        r = '%s %s %s\r\n' % (
            response_protocol, response_status, response_status_text)
        self.request.send(bytes(r, "utf-8"))
        self.request.send(bytes(response_headers_raw, "utf-8"))
        self.request.send(bytes("\r\n", "utf-8"))
        self.request.send(bytes(msg, "utf-8"))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
