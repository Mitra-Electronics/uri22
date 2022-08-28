from pytube import YouTube, request

def yt_download(url: str):
    yt = YouTube(url).streams.get_highest_resolution()
    stream = request.stream(yt.url)
    while True:
        chunk = next(stream, None)
        if chunk:
            yield chunk
        else:
            break