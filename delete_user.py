from fastapi import APIRouter
import x

router = APIRouter()

@router.delete("/users/{user_id}")
async def _(user_id):
  print(f"Deleting user with id: {user_id}")
  res = await x.db(f"DELETE {user_id}")
  return {"info":"user deleted"}
