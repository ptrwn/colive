from fastapi import FastAPI, Response
from models import Flats, FlatsGet, Users
from db import session
from sqlmodel import select
from typing import Optional, Union

app = FastAPI()


@app.get("/teapot", status_code=418)
async def teapot():
    return {"message": "I'm a teapot"}


@app.get("/flats/{flat_id}", response_model=Flats)
# @app.get("/flats/{flat_id}")
# def read_item(flat_id: int, response: Response) -> Optional[FlatsGet]:
def read_item(flat_id: int):
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
    # response.status_code = 204
    # return 


@app.get("/flats")
async def flats():
    return {"foo": "bar"}