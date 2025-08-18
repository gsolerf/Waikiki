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
