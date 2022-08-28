from pytube import YouTube, request

def yt_download(url: str):
    print(1)
    stream = request.stream(YouTube(url).streams.get_highest_resolution().url, timeout=1000)
    print(2)
    chunk = next(stream, None)
    while chunk:
        yield chunk
        chunk = next(stream, None)