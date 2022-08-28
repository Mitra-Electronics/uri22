from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from drivers.ytd import yt_download
from schemas import UR

dr = APIRouter()

@dr.post("/")
def downloader_route(url: UR):
    if 'youtube.com' in url.url.host or 'youtu.be' in url.url.host:
        return StreamingResponse(yt_download(url.url))
