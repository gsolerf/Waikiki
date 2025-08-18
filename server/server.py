from fastapi import FastAPI, WebSocket
import uvicorn
import json
from pathlib import Path

app = FastAPI()
clients = []

STATE_FILE = Path("state.json")

# Carregar l'últim estat guardat o crear un per defecte
if STATE_FILE.exists():
    with open(STATE_FILE, "r") as f:
        current_state = json.load(f)
else:
    current_state = {"type": "color", "value": "white"}

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(current_state, f)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    # Enviar l'últim estat al client que s'acaba de connectar
    await websocket.send_text(json.dumps(current_state))

    try:
        while True:
            data = await websocket.receive_text()
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''

from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                await client.send_text(data)
    except:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
