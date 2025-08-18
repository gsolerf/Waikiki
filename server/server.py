# server.py
# server.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter()
clients = []

@router.get("/server")
def server_index():
    return HTMLResponse("<h1>Servidor Server actiu. WebSocket OK.</h1>")

@router.websocket("/ws/server")
async def websocket_server(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for client in clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        clients.remove(websocket)



'''
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
clients = []

@app.get("/")
def index():
    return HTMLResponse("<h1>Servidor actiu. WebSocket OK.</h1>")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Envia el color a tots els clients connectats
            for client in clients:
                await client.send_text(data)
    except:
        clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
