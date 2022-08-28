from pytube import YouTube, request

def yt_download(url: str):
    stream = request.stream(YouTube(url).streams.get_highest_resolution().url)
    chunk = next(stream, None)
    while chunk:
        yield chunk
        chunk = next(stream, None)