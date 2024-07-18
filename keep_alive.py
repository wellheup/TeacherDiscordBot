from flask import Flask
from app import app as flask_app
from threading import Thread
import os

def run(host, port):
  # app.run(host='0.0.0.0',port=8080)
	flask_app.run(host='0.0.0.0', port=5000)

def keep_alive():
	t = Thread(target=run)
	t.start()

