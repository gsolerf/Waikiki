import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import cloudinary.uploader
import os,json

app = FastAPI()
cloudinary.config(
    cloud_name=os.getenv("Cloud_name"),
    api_key=os.getenv("Api_key"),
    api_secret=os.getenv("Api_secret")
)


# Llista de clients connectats
clients = []

# Carreguem dades inicials des de save.json o establim valors per defecte
try:
    with open("save.json", "r") as f:
        dades = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    dades = {"mode": "color", "color": "black", "text": "", "media": ""}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    # Quan un client es connecta, li enviem l’estat actual
    await websocket.send_text(json.dumps(dades))

    try:
        while True:
            # Esperem noves dades del client
            data = await websocket.receive_text()

            # Convertim a dict (ha de venir com JSON string)
            try:
                noves_dades = json.loads(data)
            except:
                continue  # si no és JSON vàlid, l’ignorem

            # Actualitzem les dades actuals
            for clau in ["mode", "color", "text", "media"]:
                if clau in noves_dades:
                    dades[clau] = noves_dades[clau]

            # Guardem a save.json
            with open("save.json", "w") as f:
                json.dump(dades, f)

            # Reenviem a tots els clients connectats
            for client in clients:
                await client.send_text(json.dumps(dades))

    except WebSocketDisconnect:
        clients.remove(websocket)

@app.get("/")
async def root():
    return {"message": "Servidor Waikiki actiu"}
