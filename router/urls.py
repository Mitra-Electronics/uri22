from fastapi import APIRouter, Header
from drivers.mongod import add_url, del_url, edit_url
from schemas import URL, URLDelete, URLEdit, URLInput

ur = APIRouter()


@ur.post("/create")
def add_url_route(data: URLInput, token=Header()):
    return URL(**add_url(data.dict(), token)).dict(exclude={'referrals', 'account_id'})


@ur.put("/update")
def update_url_route(data: URLEdit, token=Header()):
    e = edit_url(data.dict(), token)
    if e == 1:
        return {"sucess": True}


@ur.delete("/delete")
def delete_url_route(data: URLDelete, token=Header()):
    d = del_url(data.dict(), token)
    if d == 1:
        return {"sucess": True}
