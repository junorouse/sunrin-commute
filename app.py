from json import dumps
from flask import Flask, Response, send_file
from parser import get_transport_arrival

app = Flask(__name__)


@app.route("/")
def main():
    return send_file('templates/index.html')


@app.route("/js/index.js")
def js():
    return send_file('js/index.js')


@app.route("/api/get")
def api_get():
    data = dumps(get_transport_arrival())
    resp = Response(data)
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == "__main__":
    app.run(debug=True)
