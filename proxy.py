from sys import argv

from flask import Flask, request, Response
from mpi4py import MPI
from requests import Request, Session

comm = MPI.COMM_WORLD
if comm.Get_size() < 2:
    raise RuntimeError('at least two processes required')

rank = comm.Get_rank()
if rank == 0:
    if len(argv) != 2:
        print(f'usage: {argv[0]} hostname')
        exit()
    hostname = argv[1]
    app = Flask(__name__, static_folder=None)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>', methods=['GET', 'OPTIONS', 'HEAD',
                                        'POST', 'PUT', 'PATCH', 'DELETE'])
    def proxy(path):
        r = Request(
            method=request.method,
            url=request.url.replace(request.host_url, hostname),
            headers={key: value for (key, value) in request.headers
                     if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies).prepare()
        comm.send(r, dest=1)
        resp = comm.recv()
        excluded_headers = ['content-encoding', 'content-length',
                            'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.headers.items()
                   if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        return response

    app.run(host='127.0.0.1', port=42069)
elif rank == 1:
    session = Session()
    while True:
        comm.send(session.send(comm.recv()), dest=0)
