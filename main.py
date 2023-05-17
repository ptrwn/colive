import uvicorn
from fastapi import FastAPI, Response, status
from models import Flats, FlatsGet, Users
from db import session
from sqlmodel import select
from typing import Optional

app = FastAPI()

responses = {
    204: {"description": "No such item"},
    200: {"description": "OK"}
}


@app.get("/teapot", status_code=418)
async def teapot():
    return {"message": "I'm a teapot"}


@app.get("/flats/{flat_id}", response_model=FlatsGet, responses={**responses})
def read_item(flat_id: int) -> Optional[FlatsGet]:
    flat = session.exec(select(Flats).where(Flats.id==flat_id)).one_or_none()
    if flat:

        flat_details = dict()
        flat_details["name"] = flat.name
        if flat.address:
            flat_details["address"] = flat.address


        flats_users = flat.user_links

        if flats_users:

            users = []

            for ul in flats_users:
                user_details = dict()
                user = session.exec(select(Users).where(Users.id==ul.user_id)).one_or_none()
                user_details["id"] = user.id
                user_details["name"] = user.name
                user_details["role"] = ul.user_role.value
                users.append(user_details)  

            flat_details["users"] = users     

        #flats_tasks = flat.task_links


        return flat_details
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/flats")
async def flats():
    return {"foo": "bar"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)