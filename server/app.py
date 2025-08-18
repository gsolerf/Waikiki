from flask import Flask
import control
import server

app = Flask(__name__)

@app.route('/control')
def executar_control():
    return control.main()  # assumeix que tens una funció 'executar' a control.py

@app.route('/pantalla')
def executar_pantalla():
    return server.main()  # assumeix que tens una funció 'mostrar' a server.py

if __name__ == "__main__":
    app.run()
