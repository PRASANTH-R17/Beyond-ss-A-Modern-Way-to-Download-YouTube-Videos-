from django.shortcuts import render
from django.http import HttpResponse
from .models import db
import pytube
from django.http import FileResponse
from django.shortcuts import get_object_or_404
import requests

qualities = {}

# After get a URL from user. This method get available Quality and information
def select_stream(request,url):

    ytVideo = pytube.YouTube(url)

    audioQuality = ytVideo.streams.filter(type="audio", mime_type="audio/mp4").order_by("abr").desc()
    videoQuality = ytVideo.streams.filter(type="video", mime_type="video/mp4").order_by("resolution").desc()


    for stream in videoQuality:
        if stream.resolution not in qualities:
            qualities[stream.resolution] = stream
    for stream in audioQuality:
        if stream.abr not in qualities:
            qualities[stream.abr] = stream

    context = {}
    for quality in qualities:
        context[str(quality)] = [qualities[quality].type, qualities[quality].filesize_mb]
    length = ytVideo.length // 60
    obj = db()
    obj.url = url
    obj.title =ytVideo.title
    obj.save()

    return render(request, "select_stream.html", {"qualities": context, "id":obj.id,"title" : obj.title, "length" : length} )

def home(request):

    # If request have POST method it moves to Available Stream( Quality ) Page - select_stream.html page
    if request.method == "POST":
        qualities.clear()
        print("----------------Test 01")
        url = request.POST["url"]
        return (select_stream(request,url))
        #return HttpResponse(msg)

    # Starting page ( Home Page )
    print("-------------Test 02")
    return render(request,"home.html")

# It store all information in Database and start to download Video or Quality in Client System by using HttpFiieResponse
def download(request, id, quality):

    stream = qualities[quality]
    print(stream)

    obj = db.objects.get(id=id)
    obj.type=stream.type
    obj.stream=stream
    obj.quality=quality
    obj.save()


    # stream.download() - Download Path, content_type -  Content Type us
    response = FileResponse(open(stream.download("./media"), 'rb'), content_type=stream.mime_type)
    # Assign a Title for Download File
    response['Content-Disposition'] = f'attachment; filename="{obj.title}.{stream.subtype}"'

    return response

# By Changing in Youtube URL This Method is executed
def download_from_url(request):

    url=request.build_absolute_uri()
    url=url.replace("127.0.0.1:8000","www.youtube.com")
    return select_stream(request,url)


