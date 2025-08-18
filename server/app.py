# app.py
from flask import Flask
import control
import server

app = Flask(__name__)

@app.route('/executa/control')
def exec_control():
    control.main()  # O qualsevol funció

    return "Control executat!"

@app.route('/executa/server')
def exec_pantalla():
    server.main()

    return "Pantalla executada!"
