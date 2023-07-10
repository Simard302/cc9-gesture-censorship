from django.shortcuts import render
from django.http import StreamingHttpResponse
from Frontend.calc.video import VideoCensor
import tempfile, os, cv2

def index(response):
    return render(response, "index.html")
def about(response):
    return render(response, "about.html")
def contact(response):
    return render(response, "contact.html")
def streamPage(response):
    return render(response, "stream-page.html")
def uploadPage(response):
    return render(response, "upload-page.html")

def upload_stream(request):
    if request.method == 'POST' and request.FILES['video']:
        upf = request.FILES['video']
        file_src = os.path.join(tempfile._get_default_tempdir(), str(next(tempfile._get_candidate_names()))+'.avi')
        with open(file_src, 'wb+') as f:
            for chunk in upf.chunks():
                f.write(chunk)
        return StreamingHttpResponse(transform_video_stream(file_src), content_type='multipart/x-mixed-replace; boundary=frame')
    return render(request, 'upload-page.html')

def transform_video_stream(video_file):
    print('made it here')
    cap = cv2.VideoCapture(video_file, cv2.CAP_FFMPEG)
    print(cap.isOpened())
    censorer = VideoCensor()
    return censorer.calc_image(cap)