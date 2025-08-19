from fastapi import FastAPI, WebSocket, UploadFile, File
from fastapi.staticfiles import StaticFiles
import json, shutil, os

app = FastAPI()
clients = []

# Directori on guardarem fitxers pujat
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Servim els fitxers del directori media públicament
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# Carreguem dades inicials o posem per defecte
try:
    with open("save.json", "r") as f:
        dades = json.load(f)
except:
    dades = {"mode": "color", "color": "black", "text": "", "media": ""}

# Endpoint per pujar fitxers
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = os.path.join(MEDIA_DIR, file.filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # Retornem l'URL públic del fitxer
    return {"url": f"/media/{file.filename}"}

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    await websocket.send_text(json.dumps(dades))
    try:
        while True:
            data = await websocket.receive_text()
            try:
                noves_dades = json.loads(data)
            except:
                continue
            for clau in ["mode", "color", "text", "media"]:
                if clau in noves_dades:
                    dades[clau] = noves_dades[clau]
            with open("save.json", "w") as f:
                json.dump(dades, f)
            for client in clients:
                await client.send_text(json.dumps(dades))
    except:
        clients.remove(websocket)
