from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import AnyUrl

from drivers.ytd import yt_download

dr = APIRouter()

@dr.post("/")
def downloader_route(url: AnyUrl):
    if url.host == 'youtube.com' or url.host == 'youtu.be':
        return StreamingResponse(yt_download(url))
