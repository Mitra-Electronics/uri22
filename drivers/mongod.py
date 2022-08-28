from string import ascii_letters as stascii, digits as sdigits
from secrets import choice
from pathlib import Path

from fastapi import HTTPException
from pymongo import MongoClient
from pymongo.server_api import ServerApi

if (Path(__file__).parent.parent / ".web").exists():
    from config.dev import MONGODB_URL
else:
    from config.prod import MONGODB_URL
from drivers.cryptod import gen_id, hash_password, verify_password
from drivers.jwd import create_access_token, decode_access_token

client = MongoClient(MONGODB_URL, server_api=ServerApi("1"))
url_db = client.url_short

urls = url_db.urls
acc = url_db.accounts

def raise_not_found(request):
    raise HTTPException(status_code=404, detail=f"URL '{request}' doesn't exist")

def gen_key():
    id = "".join(choice(stascii+sdigits) for _ in range(6))
    if urls.find_one({"referral_id":id}) == None:
        return id
    gen_key()

def gen_acc_id():
    id = gen_id()
    if acc.find_one({"_id":id}) == None:
        return id
    gen_acc_id()

def create_acc(data: dict):
    data["hashed_password"] = hash_password(data["password"])
    data["_id"] = gen_acc_id()
    data["activated"] = False
    data["referrals_created"] = 0
    if acc.find_one(data["email"]) != None:
        raise HTTPException(status_code=266, detail=data["email"]+" already used")
    data.pop("password")
    acc.insert_one(data)
    return create_access_token({"sub":data["email"]})

def login_acc(email: str, password: str):
    account = acc.find_one({"email":email})
    if account is None:
        raise HTTPException(
        status_code=401,
        detail="Account does not exist",
    )
    if verify_password(passw=password, hashed_passw=account["hashed_password"]):
        return create_access_token({"sub":account["email"]})
    raise HTTPException(
        status_code=401,
        detail="Invalid password",
    )

def get_acc(token: str):
    dat = acc.find_one({"email":decode_access_token(token)})
    if dat is None:
        raise HTTPException(
        status_code=404,
        detail="Account does not exist",
    )
    return dat

def del_acc(token: str):
    id = get_acc(token)["id"]
    d = acc.delete_one({"_id":id})
    if d.deleted_count != 1:
        raise HTTPException(status_code=404, detail="Couldnt delete account")
    urls.delete_many({"account_id":id})

def add_url(data: dict, token: str):
    data["referral_id"] = gen_key()
    data["referrals"] = 0
    data["is_active"] = True
    t = get_acc(token)["_id"]
    data["account_id"] = t
    urls.insert_one(data)
    acc.update_one({"_id":t}, {"$inc":{"referrals_created":1}})
    return data

def get_acc_urls(acc_id: str):
    d = urls.find({"account_id":acc_id})
    for url in d:
        url.pop("account_id")
    return d
    
def fetch_url(url: str):
    dat = urls.find_one({"referral_id":url})
    if dat == None:
        raise_not_found(url)
    if not dat["is_active"]:
        raise HTTPException(status_code=403, detail="URL not active")
    if dat["payment_required"]:
        raise HTTPException(status_code=402, detail="Payment required to access URL")
    return dat["url"]

def edit_url(data: dict, token: str):
    account = get_acc(token)
    c = urls.update_one({"referral_id":data["referral_id"], "account_id":account["_id"]}, {"$set":{"url":data["url"]}})
    if c.matched_count == 0:
        raise HTTPException(status_code=404, detail="URL does not exist")
    return c.matched_count

def del_url(data: dict, token: str):
    account = get_acc(token)
    acc.update_one({"_id":account["_id"]}, {"$set":{"referrals_created":account["referrals_created"]-1}})
    c = urls.delete_one({"referral_id":data["referral_id"],"account_id":account["_id"]}).deleted_count
    if c == 0:
        raise HTTPException(status_code=404, detail="URL does not exist")
    return c
