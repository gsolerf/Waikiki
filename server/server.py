from fastapi import FastAPI, WebSocket
import uvicorn
import json  # Necessari per treballar amb JSON

app = FastAPI()
clients = []

# Intentem carregar dades inicials de save.json
try:
    with open("save.json", "r") as f:
        dades = json.load(f)
except:
    # Si no existeix, inicialitzem amb valors per defecte
    dades = {"mode": "default", "color": "white", "text": ""}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    # Quan un client es connecta, li enviem l'estat actual
    await websocket.send_text(json.dumps(dades))

    try:
        while True:
            # Rebrem noves dades del client (en format text)
            data = await websocket.receive_text()

            # Intentem convertir-les a dict JSON
            try:
                noves_dades = json.loads(data)
            except:
                continue  # si no és JSON vàlid, l'ignorem

            # Actualitzem només les claus que tenim definides
            for clau in ["mode", "color", "text"]:
                if clau in noves_dades:
                    dades[clau] = noves_dades[clau]

            # Guardem l'estat actualitzat a save.json
            with open("save.json", "w") as f:
                json.dump(dades, f)

            # Reenviem a tots els clients connectats l'estat actualitzat
            for client in clients:
                await client.send_text(json.dumps(dades))

    except:
        # Si el client es desconnecta, el traiem de la llista
        clients.remove(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
