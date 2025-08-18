import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()

STATE_FILE = Path("state.json")

# Llista de clients connectats
clients = []

# Carregar l'últim estat guardat
if STATE_FILE.exists():
    with open(STATE_FILE, "r") as f:
        current_state = json.load(f)
else:
    current_state = {"type": "color", "value": "white"}  # valor per defecte

# Funció per guardar l'estat al fitxer
def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(current_state, f)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    # Enviar l'últim estat quan es connecta un client nou
    await websocket.send_text(json.dumps(current_state))

    try:
        while True:
            data = await websocket.receive_text()
            # Actualitzar l'estat global i guardar-lo
            try:
                new_state = json.loads(data)
                current_state.update(new_state)
                save_state()
            except:
                pass  # ignorar si no és JSON vàlid

            # Enviar a tots els clients connectats
            for client in clients:
                if client != websocket:
                    await client.send_text(json.dumps(current_state))
    except:
        clients.remove(websocket)

@app.get("/")
async def root():
    return {"message": "Servidor Waikiki actiu"}

'''
import json
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

# Llista de clients connectats
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Enviar a tots els clients connectats
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except:
        clients.remove(websocket)

@app.get("/")
async def root():
    return {"message": "Servidor Waikiki actiu"}
'''


