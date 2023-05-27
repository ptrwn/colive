import uvicorn
from fastapi import FastAPI, Response, status, HTTPException
from models import Flats, FlatsGet, Users, UserInFlat
from db import session
from sqlmodel import select
from typing import Optional, Any

app = FastAPI()

responses = {
    404: {"description": "No such item"},
    200: {"description": "OK"}
}


@app.get("/teapot", status_code=418)
async def teapot():
    return {"message": "I'm a teapot"}


@app.get("/flats/{flat_id}", response_model=FlatsGet, responses={**responses})
def read_item(flat_id: Any) -> Optional[FlatsGet]:
    try:
        int(flat_id)
    except:
        return Response(status_code=status.HTTP_404_NOT_FOUND) 

    flat = session.get(Flats, flat_id)
    if flat:
        res_flat = {k: v for k, v in flat.__dict__.items() if not k.startswith('_')}
        res_flat["tasks"] = flat.tasks
        flats_users = flat.user_links
        if flats_users:
            users = [UserInFlat(id=ul.user.id, name=ul.user.name) for ul in flats_users]
            res_flat["users"] = users
        return res_flat
    
    return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/flats")
async def flats():
    return {"foo": "bar"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)