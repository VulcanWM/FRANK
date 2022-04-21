from flask import Flask
from threading import Thread
from app.views import app

def run():
    app.run(host='0.0.0.0', port=8080)

def server():
    server = Thread(target=run)
    server.start()