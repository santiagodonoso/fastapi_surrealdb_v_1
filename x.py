from fastapi import HTTPException
from fastapi.responses import JSONResponse
import httpx
from app import free_db_clients
import json

USER_MIN_LEN = 2
USER_MAX_LEN = 20

##############################
async def validate_user_name(text=""):
  text = text.strip()
  if len(text) < USER_MIN_LEN or len(text) > USER_MAX_LEN: 
    raise HTTPException(status_code=400, detail=f"user_name {USER_MIN_LEN} to {USER_MAX_LEN} characters")
  return text



##############################
async def db(q):
  try:
    db_client = free_db_clients.pop(0) if len(free_db_clients) else httpx.AsyncClient(headers={"temporal":"yes"})                          
    res = await db_client.post("http://127.0.0.1:8000/sql", auth=('admin', 'password'), data=q)
    if "temporal" not in str(db_client.headers):
      free_db_clients.append(db_client)
    else:
      db_client.aclose()
    res = json.loads(res.content)
    # print(res[-1])
    return res[-1] 
  except Exception as ex:
    status_code = ex.status_code if hasattr(ex, "status_code") else 500
    detail = ex.detail if hasattr(ex, "detail") else "something went wrong"
    return JSONResponse(status_code=status_code, content={"info":detail})
  finally:
    pass