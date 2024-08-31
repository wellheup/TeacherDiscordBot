import os
from threading import Thread
from my_flask_app import app as flask_app

def run(host, port):
    port = 80 if os.getenv("REPLIT_DEPLOYMENT") == "1" else 5000
    flask_app.run(host="0.0.0.0", port=port)


def keep_alive():
    t = Thread(target=run)
    t.start()
