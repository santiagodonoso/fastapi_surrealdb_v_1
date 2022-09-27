from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app import templates
import x

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def _(request: Request):
  users = await x.db("SELECT * FROM user")
  return templates.TemplateResponse("index.html", {"request":request, "users":users['result']})
