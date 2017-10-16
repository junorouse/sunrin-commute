from json import dumps
from flask import Flask, Response, send_file
from parser import get_transport_arrival

app = Flask(__name__)


@app.route("/")
def main():
    return send_file('templates/index.html')


@app.route("/js/<path:file_name>")
def js(file_name):
    return send_file('js/{}'.format(file_name))


@app.route("/api/get")
def api_get():
    data = dumps(get_transport_arrival())
    resp = Response(data)
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0')

