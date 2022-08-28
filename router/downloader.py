from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from drivers.ytd import yt_download
from schemas import UR

dr = APIRouter()

@dr.post("/")
def downloader_route(url: UR):
    if url.url.host == 'youtube.com' or url.url.host == 'youtu.be':
        return StreamingResponse(yt_download(url.url))
