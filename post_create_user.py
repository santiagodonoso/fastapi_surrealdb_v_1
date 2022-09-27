from fastapi import APIRouter, Form, HTTPException, Response
from fastapi.responses import JSONResponse
import httpx
from app import free_db_clients
import x
import json

router = APIRouter()

@router.post("/users")
async def create_item(response: Response, user_name: str = Form(""), user_email: str = Form("")):
  try:

    # Validate user_name
    user_namex = await x.validate_user_name(user_name)

    q = f""" LET $user_name = '{user_name}';
            LET $user_email = '{user_email}'; 
            CREATE user SET user_name=$user_name, user_email=$user_email; 
        """
    db_client = free_db_clients.pop(0) if len(free_db_clients) else httpx.AsyncClient(headers={"temporal":"yes"})                          
    res = await db_client.post("http://127.0.0.1:8000/sql", auth=('admin', 'password'), data=q)
    if "temporal" not in str(db_client.headers):
      free_db_clients.append(db_client)
    else:
      db_client.aclose()
    res = json.loads(res.content)
    print(res[-1])
    return res[-1] 
  except Exception as ex:
    status_code = ex.status_code if hasattr(ex, "status_code") else 500
    detail = ex.detail if hasattr(ex, "detail") else "something went wrong"
    return JSONResponse(status_code=status_code, content={"info":detail})
  finally:
    pass