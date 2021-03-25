from sys import argv
from flask import Flask, request, redirect, Response
import requests

app = Flask(__name__, static_folder=None)

if len(argv) != 2:
    print(f'usage: {argv[0]} hostname')
    exit()
hostname = argv[1]

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'OPTIONS', 'HEAD',
                                    'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, hostname),
        headers={key: value for (key, value) in request.headers
                 if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length',
                        'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=42069)