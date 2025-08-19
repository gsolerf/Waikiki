import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import cloudinary
import cloudinary.uploader
import os
import secrets

app = FastAPI()

# Configuració Cloudinary
cloudinary.config(
    cloud_name=os.getenv("Cloud_name"),
    api_key=os.getenv("Api_key"),
    api_secret=os.getenv("Api_secret")
)

# Autenticació bàsica
security = HTTPBasic()
USERNAME = os.getenv("WAIKIKI_USER", "admin")   # usuari des de Render
PASSWORD = os.getenv("WAIKIKI_PASS", "1234")    # contrasenya des de Render

# Llista de clients connectats
clients = []

# Carreguem dades inicials des de save.json o establim valors per defecte
try:
    with open("save.json", "r") as f:
        dades = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    dades = {"mode": "color", "color": "black", "text": "", "media": ""}

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
    except WebSocketDisconnect:
        clients.remove(websocket)

# Ruta protegida per pantalla.html
@app.get("/")
def pantalla_html(credentials: HTTPBasicCredentials = security):
    correct_user = secrets.compare_digest(credentials.username, USERNAME)
    correct_pass = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_user and correct_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencials incorrectes",
            headers={"WWW-Authenticate": "Basic"},
        )
    # Serveix pantalla.html (posar la ruta correcta segons la teva estructura)
    return FileResponse("pantalla.html")

# Ruta de prova / estat
@app.get("/status")
async def root():
    return {"message": "Servidor Waikiki actiu"}
