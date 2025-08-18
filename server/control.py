# control.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()
clients = []

@router.websocket("/ws/control")
async def websocket_control(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Envia dades a tots els clients excepte emissor
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)

@router.get("/control")
async def control_root():
    return {"message": "Servidor Control actiu"}


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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
