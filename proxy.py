from flask import Flask, request, redirect, Response
import requests

SITE_NAME = 'https://acanban.ga/'
app = Flask(__name__, static_folder=None)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'OPTIONS', 'HEAD',
                                    'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    resp = requests.request(
        method=request.method,
        url=request.url.replace(request.host_url, SITE_NAME),
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
