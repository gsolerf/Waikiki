# server.py
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
