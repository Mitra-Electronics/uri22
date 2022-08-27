from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from drivers.mongod import fetch_url
from router.account import ar
from router.urls import ur

app = FastAPI()
app.include_router(ar, prefix="/account", tags=["Account"])
app.include_router(ur, prefix="/url", tags=["Urls"])


@app.get('/')
def main():
    return "Working"


@app.get("/r/{referral_id}")
def handle(referral_id: str):
    return RedirectResponse(fetch_url(referral_id))

# "C:\Users\Ishan Miitra\.deta\bin\deta.exe"


@app.get("/R/{referral_id}")
def handle(referral_id: str):
    return RedirectResponse(fetch_url(referral_id))
