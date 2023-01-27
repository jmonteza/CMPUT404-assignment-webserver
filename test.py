# msg = "<html><body><h1>This is a test</h1><p>More content here</p></body></html>"

# response_headers = {
#     'Content-Type': 'text/html; encoding=utf8',
#     'Content-Length': len(msg),
#     'Connection': 'close',
# }

# response_headers_raw = ''.join('%s: %s\r\n' % (k, v)
#                                for k, v in response_headers.items())

# print(response_headers_raw)

# response_proto = 'HTTP/1.1'
# response_status = '200'
# response_status_text = 'OK'  # this can be random

# # sending all this stuff
# r = '%s %s %s\r\n' % (
#     response_proto, response_status, response_status_text)

# print(r)

lst = []

if lst:
    print(lst[1])
