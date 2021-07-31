import json

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional


class Bien(BaseModel):
    name_bien: str
    mota_bien: str

class Luat(BaseModel):
    name_luat: str
    mota_luat: str

class Mang(BaseModel):
    name_mang: str
    mota_mang: str
    
import giaiPhuongTrinh
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="GiaiTamGiac")
@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/cms/create", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("manager_create.html", {"request": request})

@app.get('/giaitoan/{data}')
def giaitoan(data):
    jsondata = json.loads(data)
    giaiPhuongTrinh.reset()
    print(jsondata)
    kq = giaiPhuongTrinh.run(jsondata)
    return kq

@app.post('/cms/create/save-bien')
def save_bien(item: Bien):
    return item

@app.post('/cms/create/save-luat')
def save_luat(item: Luat):
    return item

@app.post('/cms/create/save-mang')
def save_mang(item: Mang):
    return item