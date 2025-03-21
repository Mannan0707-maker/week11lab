from flask import Flask
from redis import Redis, RedisError
import os
import socket

redis = Redis(host="redis-server", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    # Fetch the correct hostname for Ansh's container
    hostname = socket.gethostname()

    # HTML template to show name and hostname
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"

    # Use the environment variable `NAME`, defaulting to "AnshPatel"
    return html.format(name=os.getenv("NAME", "AnshPatel"), hostname=hostname, visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)


