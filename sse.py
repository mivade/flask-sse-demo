"""Example of using server-sent events with Flask using gevent.

This can be run as-is using gevent's built-in WSGI server, or you can
run it with gunicorn as follows::

  gunicorn -b 127.0.0.1:5000 -k gevent sse:app

"""

import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
from numpy import random
from flask import Flask, json, Response, render_template

app = Flask(__name__)

def event():
    """For something more intelligent, take a look at Redis pub/sub
    stuff. A great example can be found here__.

    __ https://github.com/jakubroztocil/chat

    """
    while True:
        yield 'data: ' + json.dumps(random.rand(1000).tolist()) + '\n\n'
        gevent.sleep(0.2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    return Response(event(), mimetype="text/event-stream")

if __name__ == "__main__":
    WSGIServer(('', 5000), app).serve_forever()
    