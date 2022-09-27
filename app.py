from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

##############################
db_client_one = httpx.AsyncClient(headers={"Content-Type":"application/json", "ns":"company", "db":"company"}) # keep alive
db_client_two = httpx.AsyncClient(headers={"Content-Type":"application/json", "ns":"company", "db":"company"}) # keep alive
# Database pool
free_db_clients = [db_client_one, db_client_two]

##############################
import get_index
app.include_router(get_index.router)

##############################
import post_create_user
app.include_router(post_create_user.router)

##############################
import delete_user
app.include_router(delete_user.router)