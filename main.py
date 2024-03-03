#! /bin/python3
import os
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.image_gen import generate_image
from src.bg_remover import remove_background
from src.util import STATIC_PATH
from src.security import check_credentials

app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:8000", "sticker.amosgross.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
@app.get("/")
def core_frontend():
    return FileResponse("./frontend/index.html")

@app.get("/api")
def read_root():
    return {
            "status": "running"
    }

@app.get("/api/auth")
def ping_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if check_credentials(credentials.username, credentials.password):
        return {
                "status": "success"
        }
    else:
        raise HTTPException(status_code=403)

@app.get("/api/image")
def get_image_paths():
    images = os.listdir(STATIC_PATH)
    return {
            'images': images[-10:]
    }

class GenerateReqest(BaseModel):
    prompt: str

@app.post("/api/image")
def generate_sticker(req: GenerateReqest, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if check_credentials(credentials.username, credentials.password):
        filename = generate_image(req.prompt)
        remove_background("fresh." + filename, filename)
        os.remove(STATIC_PATH + "fresh." + filename)

        return {
                "link": "/static/" + filename
        }
    else:
        raise HTTPException(status_code=401)


app.mount("/", StaticFiles(directory="frontend"), name="static")
