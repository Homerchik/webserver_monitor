from flask import Flask

from tools.utils import read_config

app = Flask(__name__)


@app.route("/")
@app.route('/start')
def start():
    return "Just some default text for start page"


@app.route('/end')
def end():
    return "End page"


def run_server(config):
    (hostname, _), *_ = config.get('test').get('monitoring').items()
    host, port = hostname.split(":")
    app.run(host=host, port=port)


if __name__ == "__main__":
    run_server()