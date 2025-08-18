# app.py
from fastapi import FastAPI
from control import router as control_router
from server import router as server_router

  
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Servidor Waikiki actiu"}

app.include_router(control_router)
app.include_router(server_router)
