from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from drivers.mongod import fetch_url
from router.account import ar
from router.urls import ur
from router.downloader import dr

app = FastAPI()
app.include_router(ar, prefix="/account", tags=["Account"])
app.include_router(ur, prefix="/url", tags=["Urls"])
app.include_router(dr, prefix="/download", tags=["Download"])


@app.get('/')
def main():
    return "Working"


@app.get("/r/{referral_id}")
def handle_route(referral_id: str):
    return RedirectResponse(fetch_url(referral_id))

# "C:\Users\Ishan Miitra\.deta\bin\deta.exe"


@app.get("/R/{referral_id}")
def handle_route(referral_id: str):
    return RedirectResponse(fetch_url(referral_id))
