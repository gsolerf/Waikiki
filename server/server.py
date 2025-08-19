from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json

app = FastAPI()
clients = []

# Carreguem dades inicials o posem per defecte
try:
    with open("save.json", "r") as f:
        dades = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    dades = {"mode": "color", "color": "black", "text": "", "media": ""}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    # Enviem estat inicial al client que es connecta
    await websocket.send_text(json.dumps(dades))

    try:
        while True:
            data = await websocket.receive_text()
            try:
                noves_dades = json.loads(data)
            except:
                continue

            # Actualitzem només les claus que tenim definides
            for clau in ["mode", "color", "text", "media"]:
                if clau in noves_dades:
                    dades[clau] = noves_dades[clau]

            # Guardem sempre al JSON
            with open("save.json", "w") as f:
                json.dump(dades, f)

            # Reenviem a tots els clients
            for client in clients:
                await client.send_text(json.dumps(dades))

    except WebSocketDisconnect:
        clients.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
