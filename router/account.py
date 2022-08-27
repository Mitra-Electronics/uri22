from drivers.mongod import (create_acc, del_acc, get_acc, get_acc_urls,
                            login_acc)
from fastapi import APIRouter, Header
from schemas import AccInput, Accounts, Login

ar = APIRouter()


@ar.post("/create")
def create_account_route(data: AccInput):
    return {"token": create_acc(data.dict())}


@ar.post("/login")
def login_account_route(data: Login):
    return {"token": login_acc(data.email, data.password)}


@ar.post("/activate")
def activate_account_route(token: str):
    return {"activated":True}


@ar.post("/get")
def get_account_route(token=Header()):
    d = Accounts(**get_acc(token.token)).dict()
    d["referrals_created"] = get_acc_urls(d["account_id"])
    return d


@ar.delete("/delete")
def delete_account_route(token=Header()):
    del_acc(token.token)
    return {"deleted": True}
