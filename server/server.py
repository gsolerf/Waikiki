

from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()
clients = []

try:
    with open("save.json", "r") as f:
        dades = json.load(f)   # Carreguem el contingut del JSON (ex: {"mode": "...", "color": "..."})
except:
    # Si no existeix el JSON, inicialitzem valors per defecte
    dades = {"mode": "default", "color": "white", text: ""}


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
