# app.py
from flask import Flask
import control
import controlpantalla

app = Flask(__name__)

@app.route('/executa/control')
def exec_control():
    control.main()  # O qualsevol funció

    return "Control executat!"

@app.route('/executa/pantalla')
def exec_pantalla():
    controlpantalla.main()

    return "Pantalla executada!"
